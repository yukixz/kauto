request = require 'request'

handleResponse = (e) ->
  {method, path, body, postBody} = e.detail
  request
    method: method
    url: "http://localhost:14585" + path
    body: body
    json: true
    timeout: 4000
  .on 'error', (err) ->
    # ...
window.addEventListener 'game.response', handleResponse

module.exports =
  name: 'auto-interactor'
  displayName: 'auto-interactor'
  description: ''
  author: ''
  link: ''
  show: false
  priority: 999
  version: ''