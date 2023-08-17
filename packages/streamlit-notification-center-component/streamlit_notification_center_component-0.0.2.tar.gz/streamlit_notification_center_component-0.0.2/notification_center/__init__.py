import os
import streamlit.components.v1 as components
import streamlit as st 

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

# Create a _nc_debug value in session state that will govern debugging output
# for the component while its in use.
if '_nc_debug' not in st.session_state:
  st.session_state.setdefault('_nc_debug', False)

# Setup the storage for NotificationCenter values. 
if '_nc_data' not in st.session_state:
  st.session_state.setdefault('_nc_data', {})

def nc_get(key, default_value=None):
  """
  Retrieves the value associated with a given key from the session state.
  
  Args:
      key (str): The key for the value to retrieve.
      default_value (optional): The value to return if the key is not found. Defaults to None.

  Returns:
      The value associated with the key if found, or the default value if the key is not found.
  """
  if '_nc_data' not in st.session_state:
    st.session_state._nc_data = {}

  if st.session_state._nc_data.get(key) is not None:    
    return st.session_state._nc_data[key]
  else:
    return default_value
  
def nc_get_last(key, default_value=None):
  """
  Retrieves the value associated with a given key from the session state.
  
  Args:
      key (str): The key representing an array of messages with tis target
      default_value (optional): The value to return if the key is not found. Defaults to None.

  Returns:
      The last value for the specified `key` rather than the whole array. If no
      value is forthcoming, `default_value` is returned instead.
  """
  if '_nc_data' not in st.session_state:
    st.session_state._nc_data = {}

  if st.session_state._nc_data.get(key) != None:
    channel = st.session_state._nc_data.get(key)
    if channel:
      return channel[-1]
    else:
      return default_value 
  else:
    return default_value

def nc_get_all():
  """
  Retrieves all key-value pairs stored in the session state.
  
  Returns:
      dict: A dictionary containing all key-value pairs in the session state.
  """
  return st.session_state._nc_data

def nc_set(key, value):
  """
  Stores a value in the session state, associated with a given key.
  
  Args:
      key (str): The key to associate with the value.
      value: The value to store.
  """
  channel = st.session_state.setdefault('_nc_data', {}).setdefault(key, [])
  channel.append(value)

def nc_has(key):
  """
  Checks whether a given key exists in the session state.
  
  Args:
      key (str): The key to check for existence.

  Returns:
      bool: True if the key exists, False otherwise.
  """  
  return [False, True][nc_get(key) != None]

def nc_clear(key):
  """
  Clears the value associated with a given key in the session state.
  
  Args:
      key (str): The key for the value to clear.
  """  
  nc_get(key, []).clear()

def nc_clear_all():
  """
  Clears all key-value pairs stored in the session state.
  """
  st.session_state._nc_data = {}

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
  _component_func = components.declare_component(
    # We give the component a simple, descriptive name ("notification_center"
    # does not fit this bill, so please choose something better for your
    # own component :)
    "notification_center",

    # Pass `url` here to tell Streamlit that the component will be served
    # by the local dev server that you run via `npm run start`.
    # (This is useful while your component is in development.)
    url="http://localhost:3001",
  )
else:
  # When we're distributing a production version of the component, we'll
  # replace the `url` param with `path`, and point it to the component's
  # build directory:
  parent_dir = os.path.dirname(os.path.abspath(__file__))
  build_dir = os.path.join(parent_dir, "frontend", "build")
  _component_func = components.declare_component("notification_center", path=build_dir)

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def notification_center(key=None):
  """Create a new instance of "notification_center".

  Parameters
  ----------
  key: str or None
    An optional key that uniquely identifies this component. If this is
    None, and the component's arguments are changed, the component will
    be re-mounted in the Streamlit frontend and lose its current state.

  Returns
  -------
  dict
    A dictionary of string targets with an array of data or payloads
    from the messages in question. (This is the value passed to 
    `Streamlit.setComponentValue` on the frontend as a JSON serializable
    object.) The returned dictionary is stored in and is part of the
    st.session_state so it will persist beyond an update of the UI. If
    the message received by the notification center was added, you 
    will see its `target` key mapping to an array of `payload` data objects

  """
  component_value = _component_func(key=key)

  if component_value == None:
    return nc_get_all()

  target = component_value.get('target')  
  if component_value.get('command') is not None:
    if component_value.get('command') == 'clear':
      nc_clear(target)

    elif component_value.get('command') == 'clear-all':
      nc_clear_all()

  else:
    payload = component_value.get('payload')
    if payload is None:
      return nc_get_all()
    nc_set(target, payload)

  if st.session_state._nc_debug:    
    print(f'[NotificationCenter({key})][{target}]', nc_get(target))  

  # We could modify the value returned from the component if we wanted.
  # There's no need to do this in our simple example - but it's an option.
  return nc_get_all()

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run notification_center/__init__.py`
if not _RELEASE:
  notification_center(key="globalnc")

  has_foo = nc_has('foo')
  foo_message_count = 0
  if has_foo:
    print(nc_get('foo'))
    foo_message_count = len(nc_get('foo'))

  has_tally = nc_has('tally')
  tally_message_count = 0
  if has_tally:
    print(nc_get('tally'))
    tally_message_count = len(nc_get('tally'))

  st.components.v1.html(
    f'''
    <div>
      <p>
        <div style="color: white;">Streamlit component communication</div>
        <a class="stylized-button" onclick="sendMessage()">Send to 'foo'</a>
        <a class="stylized-button" onclick="sendMessage('tally')">Send to 'tally'</a>
        <hr/>        
        <div style="color: white;">"foo" message received count: {foo_message_count}</div>
        <div style="color: white;">"tally" message received count: {tally_message_count}</div>
        <hr/>
      </p>
    </div>

    <p>
      <a class="stylized-button" onclick="ncClearTarget('foo')">Clear 'foo'</a>
      <a class="stylized-button" onclick="ncClearTarget('tally')">Clear 'tally'</a>
      <a class="stylized-button" onclick="ncClearAll()">Clear All</a>
    </p>    

    <style>
      * {{ font-weight: 150%; }}
      a.stylized-button {{
        padding: 0.25em;
        margin: 0.1em;
        border: 1px solid slategrey;
        background-color: lightslategray;
        border-radius: 5px;
        color: lightyellow;
        cursor: pointer;
        display: inline-block;
        -webkit-user-select: none; /* Safari */
        -ms-user-select: none; /* IE 10 and IE 11 */
        user-select: none; /* Standard syntax */
      }}
    </style>
    <script>
      function sendMessage(target) {{
        ncSendMessage(target || 'foo', {{property: 'value'}})
      }}

      function ncSendMessage(target, body) {{
        Array.from(window.parent.frames).forEach((frame) => {{
          frame.postMessage({{ type: 'nc', target: target, payload: body }}, "*")
        }})
      }}

      function ncClearTarget(target) {{
        Array.from(window.parent.frames).forEach((frame) => {{
          frame.postMessage({{ type: 'nc', target: target, command: 'clear' }}, "*")
        }})
      }}

      function ncClearAll() {{
        Array.from(window.parent.frames).forEach((frame) => {{
          frame.postMessage({{ type: 'nc', command: 'clear-all' }}, "*")
        }})
      }}
    </script>
    ''', height=180
  )
