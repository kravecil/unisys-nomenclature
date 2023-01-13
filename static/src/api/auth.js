import { Cookies } from 'quasar'
import hosts from '@/api/hosts.js'
import { ref } from 'vue'

export const authenticated = ref(false)
export const user = ref({})

export const authenticate = async () => {
    console.log('Authenticating...')

    const token = Cookies.get('token')
    if (!token) {
        unauthenticate()
        return Promise.reject()
    }

    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

    authenticated.value = true

    axios.get(hosts.auth + 'api/user')
        .then(response => {
            user.value = response.data
            // user.value.canWrite = can(['shift_report_210_write'])
            // user.value.canShiftReportRead = can(['shift_report_read'])
            // user.value.canAssignmentsReportsRead = can(['assignments_reports_read'])

            console.log('Authenticated!')
            return Promise.resolve()
        })
        .catch(error => {
            console.log(error)
            return Promise.reject()
        })
}

export const unauthenticate = () => {
    console.log('Unauthenticating...')
    Cookies.remove('token', { domain: hosts.auth.hostname })
    delete axios.defaults.headers.common['Authorization']

    authenticated.value = false

    console.log('Unauthenticated!')

    window.location = hosts.home
}

export function can(abilities) {
    if (user.value.permissions?.some(item => item.name == 'administration')) return true

    for (const ability of abilities)
        if (user.value.permissions?.some(item => item.name == ability)) return true

    return false
}
