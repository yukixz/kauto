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
  .on 'response', (response) ->
    console.log "kauto sent:", path

# Set windows bounds
w = remote.getCurrentWindow()
b = w.getBounds()
b.x = b.y = 0
w.setBounds(b)

module.exports =
  name: 'kauto-interactor'
  displayName: 'kauto-interactor'
  description: ''
  author: ''
  link: ''
  show: false
  priority: 999
  version: ''
