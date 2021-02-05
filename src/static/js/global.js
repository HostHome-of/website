if ('serviceWorker' in navigator) {
    navigator.serviceWorker
    .register('/service-worker.js')
    .then(function(registration) {
        console.log('App registrada!');
        return registration;
    })
    .catch(function(err) {
        console.error('No se pudo registrar la applicacion.', err);
    });
}