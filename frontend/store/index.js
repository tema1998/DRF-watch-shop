export const state = () => ({
    products: [],
    total: [],
    next: [],
    previous: [],
    current_page: 0
})

export const mutations = {
    SET_PRODUCTS (state, products) {
        state.products = products
    },
    SET_TOTAL (state, total) {
        state.total = total
    },
    SET_NEXT (state, next) {
        state.next = next
    },
    SET_PREVIOUS (state, previous) {
        state.previous = previous
    },
    SET_CURRENT_PAGE (state, current_page) {
        state.current_page = current_page
    },
}


export const actions = {
    async cancelProducts({commit}, {query_page}) {
        let page = query_page !== undefined ? `?page=${query_page}` : '';
        const { data } = await this.$axios.get(`http://127.0.0.1:8000/api/core/products/${page}`);
        let next = data.next != null ? data.next.split('/')[5] : data.next;
        let previous = data.previous != null ? data.previous.split('/')[5] : data.previous;
        let current_page = query_page

        commit('SET_PRODUCTS', data.results)
        commit('SET_TOTAL', Math.ceil(data.count / 3))
        commit('SET_NEXT', next)
        commit('SET_PREVIOUS', previous)
        commit('SET_CURRENT_PAGE', Number(current_page))
    },
}
