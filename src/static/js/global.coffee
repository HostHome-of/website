if 'serviceWorker' of navigator
  navigator.serviceWorker.register('/service-worker.js').then((registration) ->
    console.log 'App registrada!'
    registration
  ).catch (err) ->
    console.error 'No se pudo registrar la applicacion.', err
    return
