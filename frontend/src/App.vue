<template>
  <nav>
    <router-link to="/shop">Магазин</router-link>
    <router-link to="/profile">Корзина</router-link>
    <router-link to="/auth">Авторизация</router-link>
  </nav>
  <router-view />
</template>

<style scoped lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap");

nav {
  display: flex;
  justify-content: center;
  align-items: center;

  margin: 0 auto;

  height: 150px;
  width: 100vw;

  a {
    color: #5e9269;
    font-family: "Inter", sans-serif;
    font-size: 24px;
    text-decoration: none;

    padding: 0 30px;
  }
}
</style>
