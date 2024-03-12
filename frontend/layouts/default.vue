<template>
  <div class="flex flex-col min-h-screen">
    <header>
      <Navbar />
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
};
</script>

<style>

</style>