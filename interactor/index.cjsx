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

module.exports =
  show: false
