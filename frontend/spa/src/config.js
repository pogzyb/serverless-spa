export function getBackendURL() {
    if (process.env.REACT_APP_ENVIRONMENT === 'production') {
        return 'none';
    } else {
        return 'http://localhost:8080';
    }
}