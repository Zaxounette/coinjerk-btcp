import axios from 'axios'
import api from '@/api'

const state = {
  token: localStorage.getItem('user-token') || '',
  status: '',
  user: {}
}

const getters = {
  isAuthenticated: state => !!state.token,
  authStatus: state => state.status,
}

const actions = {

  login(context, payload){
    context.commit('loginLoading')
    return api.auth.userLogin(payload)
      .then(response => {
        axios.defaults.headers.common['Authorization'] = response.data.token
        context.commit('loginSuccess', response.data.token)
      })
      .catch(error => {
        console.log(error.data) // eslint-disable-line no-console
        context.commit('loginFail')
      })
  },

  register(context, data){
    context.commit('loginLoading')
    return api.auth.userRegister(data)
      .then(response => {
        axios.defaults.headers.common['Authorization'] = response.data.token
        context.commit('loginSuccess', response.data.token)
      })
      .catch(error => {
        console.log(error.data) // eslint-disable-line no-console
        context.commit('loginFail')
      })
  },

  getUser(context){
    return api.auth.fetchUser()
      .then(response => {
        context.commit('getUserSuccessCommit', response.data)
      })
      .catch(error => {
        console.log(error.data) // eslint-disable-line no-console
        context.commit('loginFail')
      })
  },

}

const mutations = {
  getUserSuccess(state, payload) {
    state.user = payload
  },

  loginLoading(state) {
    state.status = 'loading'
  },

  loginSuccess(state, payload) {
    localStorage.setItem('user-token', payload)
    state.token = payload
    state.status = 'success'
  },

  loginFail(state) {
    localStorage.removeItem('user-token')
    state.token = ''
    state.status = 'error'
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations 
}
