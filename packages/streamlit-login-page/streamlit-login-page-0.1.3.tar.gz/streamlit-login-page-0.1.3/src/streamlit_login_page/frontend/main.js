// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  const {height} = event.detail.args;
  if (!window.rendered) {
    Streamlit.setFrameHeight(height)
    const loginBtn = document.querySelector("#login");
    loginBtn.addEventListener('click', (event) => {
      var nm=document.querySelector("#name").value;
      sendValue(nm);
    }, true);
    window.rendered = true
  }
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(1200)
