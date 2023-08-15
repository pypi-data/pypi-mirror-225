import asyncio
import socket
import functools

import aioredis

from kombu.transport.redis import (
    Transport as SyncTransport,
    Channel as SyncChannel,
    error_classes_t,
    virtual,
    InconsistencyError,
    VersionMismatch
)


def get_redis_error_classes():
    from aioredis import exceptions
    # This exception suddenly changed name between redis-py versions
    if hasattr(exceptions, 'InvalidData'):
        DataError = exceptions.InvalidData
    else:
        DataError = exceptions.DataError

    return error_classes_t(
        (virtual.Transport.connection_errors + (
            InconsistencyError,
            socket.error,
            IOError,
            OSError,
            exceptions.ConnectionError,
            exceptions.AuthenticationError,
            exceptions.TimeoutError)),
        (virtual.Transport.channel_errors + (
            DataError,
            exceptions.InvalidResponse,
            exceptions.ResponseError)),
    )


class Channel(SyncChannel):
    connection_class = aioredis.Connection
    connection_class_ssl = aioredis.SSLConnection

    def _get_client(self):
        if getattr(aioredis, 'VERSION', (1, 0)) < (2, 0, 0):
            raise VersionMismatch(
                'Redis transport requires aioredis versions 2.0.0 or later. '
                'You have {0.__version__}'.format(redis))

        if self.global_keyprefix:
            return functools.partial(
                PrefixedStrictRedis,
                global_keyprefix=self.global_keyprefix,
            )

        return redis.StrictRedis



# class Transport(SyncTransport):

