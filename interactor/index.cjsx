request = require 'request'

window.addEventListener 'game.response', (e) ->
  {method, path, body, postBody} = e.detail
  request.post
    url: "http://127.0.0.1:14585/"
    timeout: 4000
    json: true
    body:
      method: method
      path: path
      body: body
      postBody: postBody
  .on 'error', (err) ->
    return if err.code in ['ECONNREFUSED']
    console.error "kauto:", err

# Set windows bounds
w = remote.getCurrentWindow()
b = w.getBounds()
b.x = b.y = 0
w.setBounds(b)

module.exports =
  show: false
