Help on WSClient in module kubernetes.stream.ws_client object:

class WSClient(builtins.object)
 |  WSClient(configuration, url, headers, capture_all)
 |  
 |  Methods defined here:
 |  
 |  __init__(self, configuration, url, headers, capture_all)
 |      A websocket client with support for channels.
 |      
 |          Exec command uses different channels for different streams. for
 |      example, 0 is stdin, 1 is stdout and 2 is stderr. Some other API calls
 |      like port forwarding can forward different pods' streams to different
 |      channels.
 |  
 |  close(self, **kwargs)
 |      close websocket connection.
 |  
 |  is_open(self)
 |      True if the connection is still alive.
 |  
 |  peek_channel(self, channel, timeout=0)
 |      Peek a channel and return part of the input,
 |      empty string otherwise.
 |  
 |  peek_stderr(self, timeout=0)
 |      Same as peek_channel with channel=2.
 |  
 |  peek_stdout(self, timeout=0)
 |      Same as peek_channel with channel=1.
 |  
 |  read_all(self)
 |      Return buffered data received on stdout and stderr channels.
 |      This is useful for non-interactive call where a set of command passed
 |      to the API call and their result is needed after the call is concluded.
 |      Should be called after run_forever() or update()
 |      
 |      TODO: Maybe we can process this and return a more meaningful map with
 |      channels mapped for each input.
 |  
 |  read_channel(self, channel, timeout=0)
 |      Read data from a channel.
 |  
 |  read_stderr(self, timeout=None)
 |      Same as read_channel with channel=2.
 |  
 |  read_stdout(self, timeout=None)
 |      Same as read_channel with channel=1.
 |  
 |  readline_channel(self, channel, timeout=None)
 |      Read a line from a channel.
 |  
 |  readline_stderr(self, timeout=None)
 |      Same as readline_channel with channel=2.
 |  
 |  readline_stdout(self, timeout=None)
 |      Same as readline_channel with channel=1.
 |  
 |  run_forever(self, timeout=None)
 |      Wait till connection is closed or timeout reached. Buffer any input
 |      received during this time.
 |  
 |  update(self, timeout=0)
 |      Update channel buffers with at most one complete frame of input.
 |  
 |  write_channel(self, channel, data)
 |      Write data to a channel.
 |  
 |  write_stdin(self, data)
 |      The same as write_channel with channel=0.
 |  
 |  ----------------------------------------------------------------------
 |  Readonly properties defined here:
 |  
 |  returncode
 |      The return code, A None value indicates that the process hasn't
 |      terminated yet.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)