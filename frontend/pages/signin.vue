<template>
    <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
      </div>

      <div ref="wrongData" class="hidden sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 class="mt-10 text-center text-base font-bold leading-9 tracking-tight text-red-600">The password or login is incorrect!</h2>
      </div>

      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <form class="space-y-6" action="#" method="POST">
          <div>
            <label for="login" class="block text-sm font-medium leading-6 text-gray-900">Login</label>
            <div class="mt-2">
              <input v-model="login.username" id="login" name="login" type="login" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
            <div class="mt-2">
              <input v-model="login.password" id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            </div>
          </div>

          <div>
            <button @click.stop.prevent="userLogin()" type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign in</button>
          </div>
        </form>

        <p class="mt-10 text-center text-sm text-gray-500">
          Not a member?
          <nuxt-link to="/signup"  class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Sign Up</nuxt-link>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        login: {
          username: '',
          password: ''
        },
      }
    },
    methods: {
      async userLogin() {
        try {
          let response = await this.$auth.loginWith('local', { data: this.login})
          this.$router.push('/')
        } catch (err) {
          this.login.password = '';
          this.block_wrong_data = this.$refs.wrongData;
          this.block_wrong_data.classList.remove('hidden');
          console.log(this.block_wrong_data.classList)
        }
      }
    },
    head() {
        return {
        title: "Sign In - Time to buy",
        meta: [
            { hid: "description", name: "description", content: "The best watch shop!"},
            { hid: "keywords", name: "keywords", content: "watch, time, buy, money, quality"}
        ]
        }
    },
    computed: {
        user() {
        return this.$auth.user
        },
    },
  }
  </script>
  
  <style scoped>
  
  </style>