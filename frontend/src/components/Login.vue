<template>
  <form @submit.prevent="login" id="loginForm">
    <h1>Log in</h1>
    <input v-model="username" placeholder="Username" required />
    <input v-model="password" type="password" placeholder="Password" required />
    <button type="submit">Login</button>
    <p v-show="error" class="error">{{ error }}</p>
  </form>
</template>

<script>
import { loginUser } from '../scipts/api';

export default {
  name: 'Login',

  data() {
    return {
      username: '',
      password: '',
      error: null,
    };
  },

  methods: {
    async login() {
      try {
        const response = await loginUser({ username: this.username, password: this.password });
        // Сохраните токен и выполните другие действия
        localStorage.setItem('token', response.access_token);
        alert('Login successful!');
      } catch (err) {
        this.error = err.message;
      }
    },
  },
};
</script>

<style scoped lang="scss">
#loginForm {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;

  height: 100%;
  width: 100%;

  h1 {
    color: hsla(0, 0%, 9%, 0.5);
  }

  input {
    background-color: hsla(0, 0%, 9%, 0.5);
    border: none;
    outline: none;

    color: hsla(134, 22%, 47%, 1);

    padding: 5px 10px;
    margin: 30px 0 0;

    height: calc(50px - 10px);
    width: calc(90% - 20px);

    transition: all 300ms ease;
  }

  input:hover {
    background-color: hsla(0, 0%, 9%, 1);
  }

  button {
    background-color: transparent;
    border: none;
    outline: none;
    cursor: pointer;

    color: hsla(0, 0%, 9%, 0.5);
    font-weight: 700;

    align-self: end;

    padding: 5px 10px;
    margin: 30px 5% 0 0;

    height: calc(40px - 10px);
    width: calc(40% - 20px);

    transition: all 300ms ease;
  }

  button:hover {
    color: hsla(0, 0%, 9%, 1);
  }

  .error {
    margin: 50px 0 -90px;
  }
}
</style>