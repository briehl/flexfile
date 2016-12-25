import UngarView from './components/UngarView'

export default () => ({
    path: 'ungar',
    getComponent (nextState, cb) {
        require.ensure([], (require) => {
            /*  Webpack - use require callback to define
              dependencies for bundling   */
            const Ungar = require('./components/UngarView').default

            /*  Return getComponent   */
            cb(null, Ungar)
            /* Webpack named bundle   */
        }, 'ungar')
    }
})
