import os
import streamlit.components.v1 as components
import streamlit as st 

from typing import Callable

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

def nc_ensure():
  # Establish a event manager in the session_state
  if '_nc_events' not in st.session_state:
    st.session_state.setdefault('_nc_events', NCEventManager())

  # Create a _nc_debug value in session state that will govern debugging output
  # for the component while its in use.
  if '_nc_debug' not in st.session_state:
    st.session_state.setdefault('_nc_debug', False)

  # Setup the storage for NotificationCenter values. 
  if '_nc_data' not in st.session_state:
    st.session_state.setdefault('_nc_data', {})

  # Setup html, css, script defaults
  if '_nc_javascript' not in st.session_state:
    st.session_state.setdefault('_nc_javascript', [
      f'''
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
      '''
    ])

  if '_nc_styles' not in st.session_state:
    st.session_state.setdefault('_nc_styles', [])
  
  if '_nc_html' not in st.session_state:
    st.session_state.setdefault('_nc_html', [])

def nc_get(key, default_value=None):
  """
  Retrieves the value associated with a given key from the session state.
  
  Args:
      key (str): The key for the value to retrieve.
      default_value (optional): The value to return if the key is not found. Defaults to None.

  Returns:
      The value associated with the key if found, or the default value if the key is not found.
  """
  nc_ensure()

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
  nc_ensure()
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
  nc_ensure()  
  return st.session_state.get('_nc_data', {})

def nc_set(key, value):
  """
  Stores a value in the session state, associated with a given key.
  
  Args:
      key (str): The key to associate with the value.
      value: The value to store.
  """
  nc_ensure()  
  channel = st.session_state._nc_data.setdefault(key, [])
  channel.append(value)
  st.session_state._nc_events.publish(key, value)

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
  nc_ensure()  
  nc_get(key, []).clear()

def nc_clear_all():
  """
  Clears all key-value pairs stored in the session state.
  """
  nc_ensure()  
  st.session_state._nc_data = {}

def nc_add_script(script):
  """
  Adds a JavaScript snippet to the session state for inclusion in subsequent HTML rendering.

  This function allows for the addition of JavaScript code snippets to the global session state,
  which can be later utilized by the nc_html function to render within the Streamlit app.

  :param script:   A string containing the JavaScript code snippet to add.
  :return:         None.

  :example:
    nc_add_script("console.log('This script was added.');")
  """
  nc_ensure()
  st.session_state._nc_javascript.append(script)

def nc_add_style(style):
  """
  Adds a CSS snippet to the session state for inclusion in subsequent HTML rendering.

  This function allows for the addition of CSS code snippets to the global session state,
  which can be later utilized by the nc_html function to render within the Streamlit app.

  :param style:    A string containing the CSS code snippet to add.
  :return:         None.

  :example:
    nc_add_style("div { color: blue; }")
  """
  nc_ensure()
  st.session_state._nc_styles.append(style)

def nc_add_html(html):
  """
  Adds an HTML snippet to the session state for inclusion in subsequent HTML rendering.

  This function allows for the addition of HTML code snippets to the global session state,
  which can be later utilized by the nc_html function to render within the Streamlit app.

  :param html:     A string containing the HTML code snippet to add.
  :return:         None.

  :example:
    nc_add_html("<div class='added-html'>This HTML was added.</div>")
  """
  nc_ensure()
  st.session_state._nc_html.append(html)

def nc_reset_scripts():
  """
  Resets the JavaScript snippets stored in the session state.

  This function removes all JavaScript snippets added through nc_add_script, 
  returning the session state to its default without any additional scripts.

  :return:         None.
  """
  if '_nc_javascript' in st.session_state:
    del st.session_state._nc_javascript 
  nc_ensure()

def nc_reset_styles():
  """
  Resets the CSS snippets stored in the session state.

  This function removes all CSS snippets added through nc_add_style, 
  returning the session state to its default without any additional styles.

  :return:         None.
  """
  if '_nc_styles' in st.session_state:
    del st.session_state._nc_styles
  nc_ensure()

def nc_reset_html():
  """
  Resets the HTML snippets stored in the session state.

  This function removes all HTML snippets added through nc_add_html, 
  returning the session state to its default without any additional HTML snippets.

  :return:         None.
  """
  if '_nc_html' in st.session_state:
    del st.session_state._nc_html
  nc_ensure()

def nc_listen(to, callback) -> Callable:
  """
  Subscribes a callback function to a specified event within the Streamlit app's session state.

  This function associates the given callback with the specified event name within the
  session state's event manager. A lambda function is then returned, allowing for easy
  unsubscription from the event at a later time.

  :param to: The name of the event to which the callback should be subscribed. This is a string
             identifier for the event.
  :type to: str

  :param callback: The callback function to be invoked when the specified event is published.
                   The signature of this function will depend on the expected data for the event.
  :type callback: Callable

  :return: A lambda function that, when invoked, will unsubscribe the given callback from the
           specified event within the session state's event manager.
  :rtype: Callable

  :raises: This function may raise exceptions if used outside the context of a Streamlit app,
           or if there are issues with the provided parameters (e.g., invalid event name).

  :example:
    # Subscribe to an event called 'data_received'
    unsubscribe = nc_listen('data_received', lambda data: print('Data:', data))

    # Later in the code, you can call `unsubscribe()` to remove the callback
    unsubscribe()
  """  
  nc_ensure()
  st.session_state._nc_events.subscribe(to, callback)
  return lambda: st.session_state._nc_events.unsubscribe(to, callback)

# Using session state lists of css, javascript and html snippets, plus any extra 
# defined here, invoke the `st.components.v1.html` streamlit component with those
# values occurring before the supplied html. Note that the expected HTML does not
# include <head> or <!DOCTYPE> and other non-body element features. Including them
# will produce an undefined behavior.
def nc_html(html, extra_js=[], extra_css=[], width=None, height=None, scrolling=False):
  """
  Renders an HTML content block with additional JavaScript and CSS within a Streamlit app. 

  This function takes the main HTML content along with optional JavaScript and CSS snippets 
  to generate a complete HTML block. It also utilizes session state variables to provide 
  default JavaScript, CSS, and HTML snippets that are defined elsewhere in the code.

  :param html:        The main HTML content to render as a string.
  :param extra_js:    A list of additional JavaScript snippets as strings to include in the 
                      HTML. Defaults to an empty list.
  :param extra_css:   A list of additional CSS snippets as strings to include in the HTML. 
                      Defaults to an empty list.
  :param width:       The width of the HTML component within the Streamlit app. Can be an 
                      integer (pixels) or a string (e.g., "100%"). Defaults to None.
  :param height:      The height of the HTML component within the Streamlit app. Can be an 
                      integer (pixels) or a string (e.g., "100%"). Defaults to None.
  :param scrolling:   A boolean value to enable or disable scrolling within the HTML component. 
                      Defaults to False.

  :return:            None. The HTML content is rendered directly within the Streamlit app.
  :raises:            This function may raise exceptions if used outside the context of a Streamlit 
                      app or if incorrect types are provided for the parameters.

  :example:
    nc_html(
      "<div>Hello, World!</div>",
      extra_js=["console.log('Loaded!');"],
      extra_css=["div { color: red; }"],
      width="100%",
      height=200
    )
  """
  nc_ensure()
  js = '\n'.join(st.session_state._nc_javascript + extra_js)
  css = '\n'.join(st.session_state._nc_styles + extra_css)
  pre = '\n'.join(st.session_state._nc_html)

  content = f'''
    <script>{js}</script>
    <style>{css}</style>
    {pre}
    {html}
  '''
  st.components.v1.html(content, width=width, height=height, scrolling=scrolling)

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
  nc_ensure()
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

class NCEventManager:
  """
  The NCEventManager class provides an interface for managing event subscriptions,
  unsubscriptions, and publishing events. It enables a simple pub/sub pattern,
  allowing functions to be called in response to named events.

  :example:
    def on_custom_event(data):
      print("Custom event received:", data)

    manager = NCEventManager()
    manager.subscribe("custom_event", on_custom_event)
    manager.publish("custom_event", "Hello, World!")
  """

  def __init__(self):
    """
    Initializes a new instance of the NCEventManager with an empty set of listeners.
    """
    self.listeners = {}

  def subscribe(self, event_name, callback):
    """
    Subscribe to an event with a given callback function. If the event doesn't exist,
    it will be created, and the callback will be added to its listeners.

    :param event_name: The name of the event to subscribe to.
    :param callback:   The function to be called when the event is published.
    :type event_name:  str
    :type callback:    callable
    """
    if event_name not in self.listeners:
      self.listeners[event_name] = []
    self.listeners[event_name].append(callback)

  def unsubscribe(self, event_name, callback):
    """
    Unsubscribe a given callback function from an event. If the event or the callback
    does not exist, the method will do nothing.

    :param event_name: The name of the event to unsubscribe from.
    :param callback:   The function to be unsubscribed from the event.
    :type event_name:  str
    :type callback:    callable
    """
    if event_name in self.listeners:
      self.listeners[event_name].remove(callback)

  def publish(self, event_name, data=None):
    """
    Publish an event, triggering all subscribed listeners with the given data. If the event
    does not exist, the method will do nothing.

    :param event_name: The name of the event to publish.
    :param data:       Optional data to be passed to the subscribed listeners.
    :type event_name:  str
    :type data:        Any, optional
    """
    for callback in self.listeners.get(event_name, []):
      callback(data)
