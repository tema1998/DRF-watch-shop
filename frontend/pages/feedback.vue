<template>
    <div class="max-w-xl mx-auto mt-16 flex w-full flex-col border rounded-lg bg-white p-8">
        <h2 class="title-font mb-1 text-lg font-medium text-gray-900">Feedback</h2>
        <p class="mb-5 leading-relaxed text-gray-600">If you had any issues or you liked our product, please share
            with us!
        </p>

        <div class="mb-4" v-bind:class="{ 'fld-error': $v.form.name.$error }">
            <div>
                <label for="name" class="text-sm leading-7 text-gray-600">Your name</label>
                <input @input="$v.form.name.$touch()" v-model="form.name" type="text" id="name" name="name" class="w-full rounded border border-gray-300 bg-white py-1 px-3 text-base leading-8 text-gray-700 outline-none transition-colors duration-200 ease-in-out focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200" />
            </div>

            <span class="msg-error" v-if="!$v.form.name.required">
                <small>Required field.</small>
            </span>

            <span class="msg-error" v-if="!$v.form.name.minLength">
                <small>The length cannot be less than {{ $v.form.name.$params.minLength.min }} characters.</small>
            </span>
            
        </div>

        <div class="mb-4" v-bind:class="{ 'fld-error': $v.form.email.$error }">
            <div>
                <label for="email" class="text-sm leading-7 text-gray-600">Your Email</label>
                <input @input="$v.form.email.$touch()"  v-model="form.email"  type="email" id="email" name="email" class="w-full rounded border border-gray-300 bg-white py-1 px-3 text-base leading-8 text-gray-700 outline-none transition-colors duration-200 ease-in-out focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200" />
            </div>

            <span class="msg-error" v-if="!$v.form.email.required">
                <small>Required field.</small>
            </span>

            <span class="msg-error" v-if="!$v.form.email.email">
                <small>Please, enter email</small>
            </span>
            
        </div>

        <div class="mb-4" v-bind:class="{ 'fld-error': $v.form.subject.$error }">
            <div>
                <label for="subject" class="text-sm leading-7 text-gray-600">Subject</label>
                <input @input="$v.form.subject.$touch()"  v-model="form.subject" type="text" id="subject" name="subject" class="w-full rounded border border-gray-300 bg-white py-1 px-3 text-base leading-8 text-gray-700 outline-none transition-colors duration-200 ease-in-out focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200" />
            </div>

            <span class="msg-error" v-if="!$v.form.subject.required">
                <small>Required field</small>
            </span>

            <span class="msg-error" v-if="!$v.form.subject.minLength">
                <small>The length cannot be less than {{ $v.form.subject.$params.minLength.min }} characters.</small>
            </span>
            
        </div>

        <div class="mb-4" v-bind:class="{ 'fld-error': $v.form.message.$error }">
            <div>
                <label for="message" class="text-sm leading-7 text-gray-600">Message</label>
                <textarea @input="$v.form.message.$touch()"  v-model="form.message"  id="message" name="message" class="h-32 w-full resize-none rounded border border-gray-300 bg-white py-1 px-3 text-base leading-6 text-gray-700 outline-none transition-colors duration-200 ease-in-out focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200"></textarea>
            </div>
            
            <span class="msg-error" v-if="!$v.form.message.required">
                <small>Required field</small>
            </span>
        </div>
        <button class="rounded border-0 bg-indigo-500 py-2 px-6 text-lg text-white hover:bg-indigo-600 focus:outline-none" @click.prevent="submitForm" :disabled='!isComplete'>Send</button>
    </div>
</template>

<script>

import axios from "axios";
import { required, minLength, email } from 'vuelidate/lib/validators'

export default {
    data() {
    return {
      form: {
        name: '',
        email: '',
        subject: '',
        message: '',
        }
        }
    },
    methods: {
        submitForm() {
            let contactFormData = new FormData();
            contactFormData.set('name', this.form.name);
            contactFormData.set('email', this.form.email);
            contactFormData.set('subject', this.form.subject);
            contactFormData.set('message', this.form.message);
            console.log('submittting data...');
            axios({
            method: 'post',
            url: 'http://localhost:8000/api/feedback/',
            data: contactFormData
            }).then(function(response){
                console.log(response);
            }).catch(function (response){
                console.log(response);
            });
            this.$router.push("success");
        }
    },
    computed: {
      isComplete () {
        return !this.$v.$invalid;
      }
    },
    validations: {
        form: {
            name: {
            required,
            minLength: minLength( 4 )
            },
            email: {
            email,
            required
            },
            subject: {
            required,
            minLength: minLength( 2 )
            },
            message: {
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