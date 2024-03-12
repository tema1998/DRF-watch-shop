<template>
  <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Register</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-6" action="#" method="POST">
        <div>
          <label for="login" class="block text-sm font-medium leading-6 text-gray-900">Login</label>
          <div class="mt-2">
            <input v-model="register.username" id="login" name="login" type="login" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
          <div class="mt-2">
            <input v-model="register.password" id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>

        <div>
          <label for="password2" class="block text-sm font-medium leading-6 text-gray-900">Repeat password</label>
          <div class="mt-2">
            <input v-model="register.password2" id="password2" name="password2" type="password2" autocomplete="current-password" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
        </div>

        <div>
          <button @click.stop.prevent="userRegister()" type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Register</button>
        </div>
      </form>

      <p class="mt-10 text-center text-sm text-gray-500">
        Do you have an account?
        <nuxt-link to="/signin"  class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Sign In</nuxt-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      register: {
        username: '',
        password: '',
        password2: '',
      }
    }
  },
  methods: {
    async userRegister() {
      try {
        let response = await this.$axios.post('/api/register/', {
          username: this.register.username,
          password: this. register.password,
          password2: this.register.password2
        })
        console.log(response)
        await this.$auth.loginWith('local', {
          data: {
            username: this.register.username,
            password: this.register.password
          },
        })
        this.$router.push('/')
      } catch (err) {
        console.log(err)
      }
    }
  },
  head() {
        return {
        title: "Sign Up - Time to buy",
        meta: [
            { hid: "description", name: "description", content: "The best watch shop!"},
            { hid: "keywords", name: "keywords", content: "watch, time, buy, money, quality"}
        ]
        }
    },
}
</script>

<style scoped>

</style>