<template>
    <div class="max-w-xl mx-auto mt-16 flex w-full flex-col border rounded-lg bg-white p-8">
        <h2 class="title-font mb-1 text-lg font-medium text-gray-900">Feedback</h2>
        <p class="mb-5 leading-relaxed text-gray-600">If you had any issues or you liked our product, please share
            with us!
        </p>


        <div class="mb-4" v-bind:class="{ 'fld-error': $v.form.image.$error }">
            <div>
                <label for="image" class="text-sm leading-7 text-gray-600">Image</label>
                <input @input="$v.form.image.$touch()"  v-model="form.image" type="text" id="image" name="image" class="w-full rounded border border-gray-300 bg-white py-1 px-3 text-base leading-8 text-gray-700 outline-none transition-colors duration-200 ease-in-out focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200" />
            </div>

            <span class="msg-error" v-if="!$v.form.image.required">
                <small>Required field</small>
            </span>

            <span class="msg-error" v-if="!$v.form.image.minLength">
                <small>The length cannot be less than {{ $v.form.image.$params.minLength.min }} characters.</small>
            </span>
            
        </div>

        <div class="mb-4" v-bind:class="{ 'fld-error': $v.form.review.$error }">
            <div>
                <label for="review" class="text-sm leading-7 text-gray-600">Review</label>
                <textarea @input="$v.form.review.$touch()"  v-model="form.review"  id="review" name="review" class="h-32 w-full resize-none rounded border border-gray-300 bg-white py-1 px-3 text-base leading-6 text-gray-700 outline-none transition-colors duration-200 ease-in-out focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200"></textarea>
            </div>
            
            <span class="msg-error" v-if="!$v.form.review.required">
                <small>Required field</small>
            </span>
        </div>
        <button class="rounded border-0 bg-indigo-500 py-2 px-6 text-lg text-white hover:bg-indigo-600 focus:outline-none" @click.prevent="sendFeedback" :disabled='!isComplete'>Send</button>
    </div>
</template>

<script>

import axios from "axios";
import { required, minLength, email } from 'vuelidate/lib/validators'

export default {
    data() {
        return {
            form: {
                image: '',
                review: '',
            }
        }
    },
    methods: {
        async sendFeedback() {
        try {
            let response = await this.$axios.post('http://localhost:8000/api/core/feedback/', 
            {
            review: this.form.review,
            })
        console.log(response)
        } catch (err) {
            console.log(err)
        }
        this.$router.push("success");
        },
    },
    computed: {
        isComplete () {
            return !this.$v.$invalid;
        },
    },
    validations: {
        form: {
            image: {
            minLength: minLength( 2 )
            },
            review: {
            required,
            }
        }
    },

    head() {
        return {
        title: "Feedback - Time to buy",
        meta: [
            { hid: "description", name: "description", content: "The best watch shop!"},
            { hid: "keywords", name: "keywords", content: "watch, time, buy, money, quality"}
        ]
        }
    },

}
</script>

<style type="text/css">
.fld-error .msg-error  {
  display: block;
  color: #dc3545;
}
.msg-error {
  display: none;
}
</style>