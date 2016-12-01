# coding: utf-8
from __future__ import absolute_import

# Standard imports
import logging
import sys

# External imports
import aoiktracecall.config
import aoiktracecall.logging
import aoiktracecall.trace


# Traced modules should be imported after `trace_calls_in_specs` is called.


# Set configs
aoiktracecall.config.set_configs({
    # Whether use wrapper class.
    #
    # Wrapper class is more adaptive to various types of callables but will
    # break if the code that was using the original function requires a real
    # function, instead of a callable. Known cases include PyQt slot functions.
    #
    'WRAP_USING_WRAPPER_CLASS': True,

    # Whether wrap base class attributes in a subclass.
    #
    # If enabled, wrapper attributes will be added to a subclass even if the
    # wrapped original attributes are defined in a base class.
    #
    # This helps in the case that base class attributes are implemented in C
    # extensions thus can not be traced directly.
    #
    'WRAP_BASE_CLASS_ATTRIBUTES': True,

    # Indentation unit text
    'INDENT_UNIT_TEXT': ' ' * 8,

    # Whether highlight title shows `self` argument's class instead of called
    # function's defining class.
    #
    # This helps reveal the real type of the `self` argument on which the
    # function is called.
    #
    'HIGHLIGHT_TITLE_SHOW_SELF_CLASS': True,

    # Highlight title line character count max
    'HIGHLIGHT_TITLE_LINE_CHAR_COUNT_MAX': 265,

    # Whether show main thread ID
    'SHOW_MAIN_THREAD_ID': False,

    # Whether show function's file path and line number in pre-call hook
    'SHOW_FUNC_FILE_PATH_LINENO_PRE_CALL': True,

    # Whether show function's file path and line number in post-call hook
    'SHOW_FUNC_FILE_PATH_LINENO_POST_CALL': False,

    # Whether wrapper function should debug info dict's URIs
    'WRAPPER_FUNC_DEBUG_INFO_DICT_URIS': False,

    # Whether printing handler should debug arguments inspect info
    'PRINTING_HANDLER_DEBUG_ARGS_INSPECT_INFO': False,

    # Whether printing handler should debug info dict.
    #
    # Notice info dict contains called function's arguments and printing these
    # arguments may cause errors.
    #
    'PRINTING_HANDLER_DEBUG_INFO_DICT': False,

    # Whether printing handler should debug info dict, excluding arguments.
    #
    # Use this if `PRINTING_HANDLER_DEBUG_INFO_DICT` causes errors.
    #
    'PRINTING_HANDLER_DEBUG_INFO_DICT_SAFE': False,
})


# Add debug logger handler
aoiktracecall.logging.get_debug_logger().addHandler(logging.NullHandler())

# Add info logger handler
aoiktracecall.logging.get_info_logger().addHandler(
    logging.StreamHandler(sys.stdout)
)

# Add error logger handler
aoiktracecall.logging.get_error_logger().addHandler(
    logging.StreamHandler(sys.stderr)
)


# Constant for `highlight`
HL = 'highlight'

# Create trace specs.
#
# The order of the specs determines the matching precedence, with one exception
# that URI patterns consisting of only alphanumerics, underscores, and dots are
# considered as exact URI matching, and will have higher precedence over all
# regular expression matchings. The rationale is that a spec with exact URI
# matching is more specific therefore should not be shadowed by any spec with
# regular expression matching that has appeared early.
#
trace_specs = [
    # ----- aoiktracecall -----
    ('aoiktracecall([.].+)?', False),

    # ----- * -----
    # Tracing `__setattr__` will reveal instances' attribute assignments.
    # Notice Python 2 old-style classes have no `__setattr__` attribute.
    ('.+[.]__setattr__', False),

    # Not trace most of double-underscore functions.
    # Tracing double-underscore functions is likely to break code, e.g. tracing
    # `__str__` or `__repr__` may cause infinite recursion.
    ('.+[.]__(?!init|call)[^.]+__', False),

    # ----- socket._socketobject (Python 2), socket.socket (Python 3) -----
    # Notice in Python 2, class `socket._socketobject`'s instance methods
    # - recv
    # - recvfrom
    # - recv_into
    # - recvfrom_into
    # - send
    # - sendto
    # are dynamically generated in `_socketobject.__init__`. The approach of
    # wrapping class attributes is unable to trace these methods.

    ('socket[.](_socketobject|socket)[.]__init__', HL),

    ('socket[.](_socketobject|socket)[.]bind', HL),

    ('socket[.](_socketobject|socket)[.]listen', HL),

    ('socket[.](_socketobject|socket)[.]connect', HL),

    ('socket[.](_socketobject|socket)[.]accept', HL),

    ('socket[.](_socketobject|socket)[.]setblocking', HL),

    ('socket[.](_socketobject|socket)[.]setsockopt', HL),

    ('socket[.](_socketobject|socket)[.]settimeout', HL),

    ('socket[.](_socketobject|socket)[.]makefile', HL),

    ('socket[.](_socketobject|socket)[.]recv.*', HL),

    ('socket[.](_socketobject|socket)[.]send.*', HL),

    ('socket[.](_socketobject|socket)[.]shutdown', HL),

    ('socket[.](_socketobject|socket)[.]close', HL),

    # ----- socket._fileobject (Python 2), socket.SocketIO (Python 3) -----
    ('socket[.](SocketIO|_fileobject)[.]__init__', HL),

    ('socket[.](SocketIO|_fileobject)[.]readable', True),

    ('socket[.](SocketIO|_fileobject)[.]read.*', HL),

    ('socket[.](SocketIO|_fileobject)[.]writable', True),

    ('socket[.](SocketIO|_fileobject)[.]write.*', HL),

    ('socket[.](SocketIO|_fileobject)[.]flush', HL),

    ('socket[.](SocketIO|_fileobject)[.]close', HL),

    ('socket[.](SocketIO|_fileobject)[.].+', True),

    # ----- socket -----
    ('socket._intenum_converter', False),

    ('socket[.].+[.]_decref_socketios', False),

    ('socket[.].+[.]fileno', False),

    # Ignore to avoid error in `__repr__` in Python 3
    ('socket[.].+[.]getpeername', False),

    # Ignore to avoid error in `__repr__` in Python 3
    ('socket[.].+[.]getsockname', False),

    ('socket[.].+[.]gettimeout', False),

    ('socket([.].+)?', True),

    # ----- select (Python 2) -----
    ('select.select', HL),

    ('select([.].+)?', True),

    # ----- selectors (Python 3) -----
    ('selectors.SelectSelector.__init__', HL),

    ('selectors.SelectSelector.register', HL),

    ('selectors.SelectSelector.select', HL),

    ('selectors([.].+)?', True),

    # ----- SocketServer (Python 2), socketserver (Python 3) -----
    ('SocketServer._eintr_retry', False),

    ('(socketserver|SocketServer)[.]BaseServer[.]__init__', HL),

    ('(socketserver|SocketServer)[.]TCPServer[.]__init__', HL),

    ('(socketserver|SocketServer)[.]ThreadingMixIn[.]process_request', HL),

    (
        '(socketserver|SocketServer)[.]ThreadingMixIn[.]'
        'process_request_thread', HL
    ),

    # Ignore to avoid error:
    # ```
    # 'WSGIServer' object has no attribute '_BaseServer__is_shut_down'
    # ```
    ('(socketserver|SocketServer)[.]ThreadingMixIn[.].+', False),

    ('(socketserver|SocketServer)[.]BaseRequestHandler[.]__init__', HL),

    ('(socketserver|SocketServer)[.].+[.]service_actions', False),

    ('.+[.]server_bind', HL),

    ('.+[.]server_activate', HL),

    ('.+[.]serve_forever', HL),

    ('.+[.]_handle_request_noblock', HL),

    ('.+[.]get_request', HL),

    ('.+[.]verify_request', HL),

    ('.+[.]process_request', HL),

    ('.+[.]process_request_thread', HL),

    ('.+[.]finish_request', HL),

    ('.+[.]setup', HL),

    ('.+[.]handle', HL),

    ('.+[.]finish', HL),

    ('.+[.]shutdown_request', HL),

    ('.+[.]close_request', HL),

    ('.+[.]fileno', False),

    ('(socketserver|SocketServer)([.].+)?', True),

    # ----- asyncio -----
    ('asyncio.base_events.BaseEventLoop._call_soon', HL),

    ('asyncio.base_events.BaseEventLoop._check_closed', False),

    ('asyncio.base_events.BaseEventLoop._create_server_getaddrinfo', HL),

    ('asyncio.base_events.BaseEventLoop._run_once', HL),

    ('asyncio.base_events.BaseEventLoop.call_soon', HL),

    ('asyncio.base_events.BaseEventLoop.create_future', HL),

    ('asyncio.base_events.BaseEventLoop.create_server', HL),

    ('asyncio.base_events.BaseEventLoop.create_task', HL),

    ('asyncio.base_events.BaseEventLoop.run_forever', HL),

    ('asyncio.base_events.BaseEventLoop.run_until_complete', HL),

    ('asyncio.base_events.Server.__init__', HL),

    ('asyncio.base_events.Server._detach', HL),

    ('asyncio.base_events.Server._wakeup', HL),

    ('asyncio.base_events.Server.wait_closed', HL),

    ('asyncio.base_events._ensure_resolved', HL),

    ('asyncio.base_events._ipaddr_info', HL),

    ('asyncio.base_events._run_until_complete_cb', HL),

    ('asyncio.coroutines.iscoroutine', False),

    ('asyncio.coroutines.iscoroutinefunction', False),

    # Ignore to avoid error
    ('asyncio.coroutines._format(.+)', False),

    # Ignore to avoid error
    ('asyncio.events._format(.+)', False),

    ('asyncio.events.Handle.__init__', HL),

    ('asyncio.events.Handle._run', HL),

    ('asyncio.events._get_function_source', False),

    ('asyncio.events.new_event_loop', HL),

    ('asyncio.events.set_event_loop', HL),

    ('asyncio.futures.Future._Future__format_callbacks', False),

    ('asyncio.futures.Future.__init__', HL),

    ('asyncio.futures.Future._schedule_callbacks', HL),

    ('asyncio.futures.Future.add_done_callback', HL),

    ('asyncio.futures.Future.set_result', HL),

    ('asyncio.futures._set_result_unless_cancelled', HL),

    ('asyncio.protocols.BaseProtocol.connection_lost', HL),

    ('asyncio.protocols.Protocol.eof_received', HL),

    ('asyncio.selector_events.BaseSelectorEventLoop._accept_connection', HL),

    ('asyncio.selector_events.BaseSelectorEventLoop._accept_connection2', HL),

    ('asyncio.selector_events.BaseSelectorEventLoop._make_socket_transport',
        HL),

    ('asyncio.selector_events.BaseSelectorEventLoop._process_events', HL),

    ('asyncio.selector_events.BaseSelectorEventLoop._start_serving', HL),

    ('asyncio.selector_events.BaseSelectorEventLoop._stop_serving', HL),

    ('asyncio.selector_events.BaseSelectorEventLoop.add_reader', HL),

    ('asyncio.selector_events.BaseSelectorEventLoop.remove_reader', HL),

    ('asyncio.selector_events.BaseSelectorEventLoop.remove_writer', HL),

    ('asyncio.selector_events._SelectorSocketTransport.__init__', HL),

    ('asyncio.selector_events._SelectorSocketTransport._read_ready', HL),

    ('asyncio.selector_events._SelectorSocketTransport.write', HL),

    ('asyncio.selector_events._SelectorTransport.__init__', HL),

    ('asyncio.selector_events._SelectorTransport._call_connection_lost', HL),

    ('asyncio.selector_events._SelectorTransport.close', HL),

    ('asyncio.selector_events._SelectorTransport.get_write_buffer_size',
        False),

    ('asyncio.selector_events._test_selector_event', 'hide_tree'),

    ('asyncio.tasks.Task -> asyncio.futures.Future.__init__', HL),

    ('asyncio.tasks.Task.__init__', HL),

    ('asyncio.tasks.Task._step', HL),

    ('asyncio.tasks.Task._wakeup', HL),

    ('asyncio.tasks._GatheringFuture.__init__', HL),

    ('asyncio.tasks.ensure_future', HL),

    ('asyncio.tasks.gather', HL),

    ('asyncio.transports.BaseTransport.__init__', HL),

    ('asyncio.transports._FlowControlMixin.__init__', HL),

    # Ignore to avoid error
    ('asyncio[.](.+)[.]_repr_info', False),

    ('asyncio[.](.+)[.]get_debug', False),

    ('asyncio[.](.+)[.]is_closed', False),

    ('asyncio[.](.+)[.]is_running', False),

    ('asyncio([.].+)?', True),

    # ----- __main__ -----
    ('__main__', True),

    ('__main__.main', HL),

    ('__main__.EchoProtocol', True),

    ('__main__.EchoProtocol.connection_made', HL),

    ('__main__.EchoProtocol.data_received', HL),
]


# Trace calls according to trace specs.
#
# This function will hook the module importing system in order to intercept and
# process newly imported modules. Callables in these modules which are matched
# by one of the trace specs will be wrapped to enable tracing.
#
# Already imported modules will be processed as well. But their callables may
# have been referenced elsewhere already, making the tracing incomplete. This
# explains why import hook is needed and why modules must be imported after
# `trace_calls_in_specs` is called.
#
aoiktracecall.trace.trace_calls_in_specs(specs=trace_specs)


# Import modules after `trace_calls_in_specs` is called
import asyncio
import socket


class EchoProtocol(asyncio.Protocol):
    """
    This protocol echoes request body in response body.
    """

    def connection_made(self, transport):
        """
        This callback is called when connection is established.
        """
        # Store transport object
        self.transport = transport

    def data_received(self, data):
        """
        This callback is called when data are received.
        """
        # Write response data
        self.transport.write(data)

        # Close connection
        self.transport._sock.shutdown(socket.SHUT_WR)

        # Close server
        self.transport._server.close()


def main():
    try:
        # Create event loop
        event_loop = asyncio.new_event_loop()

        # Set as global event loop
        asyncio.set_event_loop(event_loop)

        # Create coroutine `create_server`
        create_server_coro = event_loop.create_server(
            EchoProtocol, '127.0.0.1', 8000
        )

        # Create server
        server = event_loop.run_until_complete(create_server_coro)

        # Create coroutine `wait_closed`
        wait_closed_coro = server.wait_closed()

        # Run until server is closed
        event_loop.run_until_complete(wait_closed_coro)

    # If have `KeyboardInterrupt`
    except KeyboardInterrupt:
        # Stop gracefully
        pass


# Trace calls in this module.
#
# Calling this function is needed because at the point `trace_calls_in_specs`
# is called, this module is being initialized, therefore callables defined
# after the call point are not accessible to `trace_calls_in_specs`.
#
aoiktracecall.trace.trace_calls_in_this_module()


# If is run as main module
if __name__ == '__main__':
    # Call main function
    exit(main())
