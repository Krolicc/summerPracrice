<template>
  <div id="commonForm">
    <nav>
      <button @click="this.changeMethod">Login</button>
      <button @click="this.changeMethod">Sign in</button>
    </nav>
    <Login v-if="this.isLogIn"/>
    <Register v-if="!this.isLogIn"/>
  </div>
</template>

<script>
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';

export default {
  data() {
    return {
      isLogIn: false,
    };
  },

  methods: {
    changeMethod() {
      this.isLogIn = !this.isLogIn; 
    },
  },

  components: {
    Login, 
    Register,
  }
};
</script>

<style scoped lang="scss">
#commonForm {
  background-color: hsla(134, 22%, 47%, 1);

  border-radius: 15px;

  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;

  position: absolute;
  top: calc(50% - 250px);
  left: calc(50% - 150px);

  padding: 20px 10px;

  height: 300px;
  width: 300px;

  nav {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;

    margin-top: -90px;
    margin-bottom: 40px;

    height: 50px;
    width: 100%;

    button {
      background-color: transparent;
      border: none;

      font-size: 1.25em;
      
      color: hsla(134, 22%, 47%, 1)
    }
  }
}
</style>