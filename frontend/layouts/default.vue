<template>
  <div class="flex flex-col min-h-screen">
    <header>
      <Navbar :orderPrice="orderPrice" @count-cart-after-add-product="countCartAfterAddProduct" @count-cart-after-remove-product="countCartAfterRemoveProduct" />
    </header>

    <main class="grow">
      <Nuxt />
    </main>

    <Footer />

  </div>
</template>


<script>
import Navbar from "~/components/Navbar";
import Footer from "~/components/Footer";


export default {
  created() {
    this.$nuxt.$on('count-cart-after-add-product', ($event) => this.countCartAfterAddProduct($event))
    this.$nuxt.$on('count-cart-after-remove-product', ($event) => this.countCartAfterRemoveProduct($event))

  },

  data() {
      return {
        orderPrice: 0,
      }
  },

  async fetch() {
    try {
      let cart  = await this.$axios.get('http://localhost:8000/api/core/cart/')
      this.orderPrice = cart.data.order_price;
    } catch (err) {
        console.log(err);
    };
  },

  methods: {
    countCartAfterAddProduct(product_price) {
      this.orderPrice += Number(product_price);
    },

    countCartAfterRemoveProduct(product_price) {
      this.orderPrice -= Number(product_price);
    },
  },

  components: {
    Navbar,
    Footer,
  },

  head() {
    return {
      link: [
        { rel: "canonical", href: `http://localhost:3000${this.$route.path}`}
      ]
    }
  },
}
</script>

<style>

</style>