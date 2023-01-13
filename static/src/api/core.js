import axios from 'axios'
import { stats } from '@/api/store'

/**
 * Получаем статистику в header (количество номенклатурных и заявок)
 */
export const refreshStats = async () => {
    const response = await axios.get('/api/requests/stats')
    stats.value = {
        products: response.data.products,
        requests: response.data.requests,
    }
    return Promise.resolve(1)
}

/**
 * Получаем сводную информацию (последние добавленные, самые просматриваемые и т.п.)
 */
export const getSummary = async () => {
    const response = await axios.get('/api/requests/summary')

    return Promise.resolve({
        recentApproved: response.data.recent_approved,
        recentCreated: response.data.recent_created,
        mostPopular: response.data.most_popular,
    })
}

/**
 * Все номенклатурные номера по изделиям
 */
export const getProducts = async ({page, group, search} = {}) => {
    const response = await axios(`/api/products/?page=${page}&search=${search}&group=${group}`)

    return Promise.resolve(response.data)
}

/** 
 * Все группы для дерева
 */
export const getGroups = async () => {
    const response = await axios('/api/groups')
    
    return Promise.resolve(response.data)
}

/**
 * Все заявки
 */
export const getRequests = async (page=1) => {
    const response = await axios(`/api/requests?page=${page}`)

    return Promise.resolve(response.data)
}