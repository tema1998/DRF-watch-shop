<template>
  <div v-if="loggedIn != false">

    <div class="flex flex-col lg:flex-row lg:justify-around justify-center lg:items-stretch items-center mt-5">
      <div v-for="product in products" :key="product.product.slug" class="flex flex-col justify-between  my-2 lg:my-0 w-full max-w-sm bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-600 dark:border-gray-700">
        <div class="flex justify-center items-center ">
          <nuxt-link :to="`/products/${product.product.slug}`" >
            <img class="p-8 rounded-t-lg max-h-96" :src="product.product.image" alt="product image" />
          </nuxt-link>
        </div>
        <div class="px-5 pb-5">
            <nuxt-link :to="`/products/${product.product.slug}`" >
                <h5 class="text-xl font-semibold tracking-tight text-gray-900 dark:text-white">{{ product.product.model }}</h5>
            </nuxt-link>

            <div class="flex justify-between">
              <div class="flex items-center mt-2.5 mb-5">
                <div class="flex items-center space-x-1 rtl:space-x-reverse">
                    <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                        <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                    </svg>
                    <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                        <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                    </svg>
                    <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                        <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                    </svg>
                    <svg class="w-4 h-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                        <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                    </svg>
                    <svg class="w-4 h-4 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                        <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                    </svg>
                </div>
                <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded dark:bg-blue-200 dark:text-blue-800 ms-3">5.0</span>
              </div>
              <div>
              Quantity: {{product.quantity }}
              </div>
            </div>

            <div class="flex items-center justify-between">
                <span class="text-3xl font-bold text-gray-900 dark:text-white">${{ product.product.price }} </span>
                <a href="#" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Add to cart</a>
            </div>
        </div>
      </div>
    </div>

    <div class="flex flex-col m-5 justify-center items-center">
      <div class="py-5">
      <span class="font-medium">Total price:</span> <span class="font-bold"> {{order_price}} </span>
      </div>

      <div>
        <div v-if="payment_url === null">
          <a @click.prevent="create_payment()" href="#" class="text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:outline-none focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-800">Create payment</a>
        </div>

        <div v-else :key="payment_url"> 
          <a @click.prevent="redirectToPaymentUrl()" class="text-white bg-orange-700 hover:bg-orange-800 focus:ring-4 focus:outline-none focus:ring-orange-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-orange-600 dark:hover:bg-orange-700 dark:focus:ring-orange-800">Payment page</a>
          <a @click.prevent="cancel_payment()" href="#" class="text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800">Cancel payment</a>
        </div>
      </div>

    </div>
    
  </div>

  <div v-else class="flex justify-center items-center p-10">
    <nuxt-link to="/signin" >Sign In </nuxt-link> 
    <span>&nbsp; or &nbsp;</span>
    <nuxt-link to="/signup" >Sign Up </nuxt-link> 
    <span>&nbsp; to add products to cart.</span>
  </div>

</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      products: [],
      order_price: 0,
      current_page: 0,
      payment_url: null,
    }
  },

  async asyncData({$axios}) {
    try {
        let { data }  = await $axios.get('http://localhost:8000/api/core/cart/')
        if (data.payment_process) {
          data =
          {
            products: data.ordered_products,
            order_price: data.order_price,
            payment_url: data.payment_process.payment_url,
          }
        }
        else {
          data =
          {
            products: data.ordered_products,
            order_price: data.order_price,
            payment_url: null,
          }
        }
        return data
    } catch (err) {
        console.log(err)
    };
  },

  head() {
    return {
      title: "Time to buy - watch shop!",
      meta: [
        { hid: "description", name: "description", content: "The best watch shop!"},
        { hid: "keywords", name: "keywords", content: "watch, time, buy, money, quality"}
      ]
    }
  },

  methods: {

    async redirectToPaymentUrl() {
       window.location.replace(this.payment_url)
    },

    async create_payment() {
      try {
          let response = await this.$axios.post('http://localhost:8000/api/payment/create/',
            {return_url: 'http://localhost:3000/cart'}
          )
          this.payment_url = response.data.payment_url;
      } catch (err) {
          console.log(err)
      }
      },

    async cancel_payment() {
      try {
          let response = await this.$axios.post('http://localhost:8000/api/payment/cancel/')
          this.payment_url = null;
      } catch (err) {
          console.log(err)
      }
      },

  },

  computed: {
      loggedIn() {
        return this.$auth.loggedIn
      },
  },

}

</script>

<style>

</style>