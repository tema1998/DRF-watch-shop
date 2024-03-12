<template>
    <section class="bg-white dark:bg-gray-900 py-8 lg:py-16 antialiased">
        <div class="max-w-2xl mx-auto px-4">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-lg lg:text-2xl font-bold text-gray-900 dark:text-white">Reviews</h2>
            </div>

            <div v-if="loggedIn">
                <form @submit.prevent="addComment" class="mb-6">
                    <div class="py-2 px-4 mb-4 bg-white rounded-lg rounded-t-lg border border-gray-200 dark:bg-gray-800 dark:border-gray-700">
                        <label for="comment" class="sr-only">Your review</label>
                        <textarea v-model="new_review" id="comment" rows="6"
                            class="px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 focus:outline-none dark:text-white dark:placeholder-gray-400 dark:bg-gray-800"
                            placeholder="Write a review..." required></textarea>
                    </div>
                    <button :disabled='!isComplete' type="submit"
                        class="inline-flex items-center py-2.5 px-4 text-xs font-medium text-center bg-slate-500 text-white bg-primary-700 rounded-lg focus:ring-4 focus:ring-primary-200 dark:focus:ring-primary-900 hover:bg-primary-800">
                        Post review
                    </button>
                </form>
            </div>
            <div v-else>
                <h6 class=""><nuxt-link to="/signin">Sign in</nuxt-link> or <nuxt-link to="/signup">sign up</nuxt-link> to comment it!</h6>
            </div>


            <article v-for="review in reviews" :key="review.id" class="p-6 text-base bg-white rounded-lg dark:bg-gray-900">
                <footer class="flex justify-between items-center mb-2">
                    <div class="flex items-center">
                        <p class="inline-flex items-center mr-3 text-sm text-gray-900 dark:text-white font-semibold">{{ review.username }}</p>
                        <p class="text-sm text-gray-600 dark:text-gray-400"><time pubdate datetime="2022-02-08"
                                title="February 8th, 2022">{{ review.created_date }}</time></p>
                    </div>
                </footer>
                <p class="text-gray-500 dark:text-gray-400">{{ review.text }}</p>
            </article>
            
        </div>
    </section>
</template>

<script>
export default {
    props: ['reviews', 'product'],
    data() {
        return {
        new_review: '',
        }
    },
    methods: {
        async addComment() {
        try {
            let response = await this.$axios.post('http://localhost:8000/api/reviews/', {
            product: this.$props.product.slug,
            username: this.user.username,
            text: this.new_review,
        })
            this.new_review = '';
            this.reviews.splice(0, 0, response.data)
        console.log(response)
        } catch (err) {
            console.log(err)
        }
        },
    },
    computed: {
        loggedIn() {
        return this.$auth.loggedIn
        },
        user() {
        return this.$auth.user
        },
        isComplete () {
        return this.new_review;
        }
    }
}
</script>

<style scoped>

</style>