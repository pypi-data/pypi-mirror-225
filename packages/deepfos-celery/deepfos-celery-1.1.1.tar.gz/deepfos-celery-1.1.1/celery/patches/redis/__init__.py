from typing import Optional

import redis.asyncio as aioredis

from redis.asyncio.cluster import (
    RedisCluster,
    ClusterNode,
)
from redis.asyncio.client import PubSub, Lock
from redis.commands.core import AsyncPubSubCommands


__all__ = ('apply_patch', )


class ClusterConnectionPool(aioredis.ConnectionPool):
    """
    A connection pool wraps ClusterNode to
    mimic redis.asyncio.ConnectionPool
    """

    def __init__(
        self,
        node: ClusterNode,
        cluster: RedisCluster,
        connection_class=aioredis.Connection,
        max_connections: Optional[int] = None,
        **connection_kwargs,
    ):
        super().__init__(
            connection_class, max_connections, **connection_kwargs)
        self.node = node
        self.cluster = cluster

    async def get_connection(self, command_name, *keys, **options):
        return self.node.acquire_connection()

    def get_encoder(self):
        return self.cluster.get_encoder()

    def make_connection(self):
        node = self.node
        return node.connection_class(**node.connection_kwargs)

    async def release(self, connection: aioredis.Connection):
        self.node._free.append(connection)

    async def disconnect(self, inuse_connections: bool = True):
        await self.node.disconnect()


class ClusterPubSub(PubSub):
    cluster: RedisCluster

    def __init__(self, redis_cluster, **kwargs):
        """
        When a pubsub instance is created without specifying a node, a single
        node will be transparently chosen for the pubsub connection on the
        first command execution. The node will be determined by:
         1. Hashing the channel name in the request to find its keyslot
         2. Selecting a node that handles the keyslot: If read_from_replicas is
            set to true, a replica can be selected.

        :type redis_cluster: RedisCluster
        """
        self.node = None
        self.cluster = redis_cluster
        super().__init__(
            **kwargs, connection_pool=None,
            encoder=redis_cluster.encoder
        )

    async def execute_command(self, *args, **kwargs):
        if self.connection is None:
            if self.connection_pool is None:
                if self.cluster._initialize:
                    await self.cluster.initialize()

                if len(args) > 1:
                    # Hash the first channel and get one of the nodes holding
                    # this slot
                    channel = args[1]
                    node = self.cluster.get_node_from_key(
                        channel, self.cluster.read_from_replicas)
                else:
                    # Get a random node
                    node = self.cluster.get_random_node()
                self.node = node
                self.connection_pool = ClusterConnectionPool(
                    node, self.cluster)
            self.connection = await self.connection_pool.get_connection('_')
            # register a callback that re-subscribes to any channels we
            # were listening to when we were disconnected
            self.connection.register_connect_callback(self.on_connect)
        connection = self.connection
        await self._execute(connection, connection.send_command, *args)


class ConnectionPool:
    def __init__(self, cluster: RedisCluster):
        self.cluster = cluster

    def get_encoder(self):
        return self.cluster.get_encoder()


class PatchedCluster(RedisCluster, AsyncPubSubCommands):
    def __init__(self, *args, **kwargs):
        kwargs.pop('retry_on_timeout', None)
        max_conns = kwargs.pop('max_connections', None)
        if max_conns is not None:
            kwargs['max_connections'] = max_conns
        super().__init__(*args, **kwargs)
        self.connection_pool = ConnectionPool(self)

    def pubsub(self,  **kwargs):
        return ClusterPubSub(self, **kwargs)

    async def publish(self, channel, message, **kwargs):
        async with self.pubsub() as pubsub:
            return await pubsub.execute_command(
                'PUBLISH', channel, message, **kwargs)

    def lock(
        self,
        name,
        timeout: Optional[float] = None,
        sleep: float = 0.1,
        blocking_timeout: Optional[float] = None,
        thread_local: bool = True,
    ) -> Lock:
        return Lock(
            self,
            name,
            timeout=timeout,
            sleep=sleep,
            blocking_timeout=blocking_timeout,
            thread_local=thread_local,
        )


def apply_patch():
    from redis.asyncio import cluster

    cluster.RedisCluster = PatchedCluster
