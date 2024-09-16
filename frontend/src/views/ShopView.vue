<template>
  <div class="items">
    <div v-for="(el, idx) in this.items" :key="idx" class="item" @click="this.add_item(idx + 1)">
      <div class="data">
        <p class="name">{{ el.name }}</p>
        <p class="price">{{ el.price }}</p>
      </div>
    </div>
  </div>
  
  <div class="statusBlock_wrapper"></div>
</template>

<script>
import axios from "axios";

export default {
  name: "ShopView",

  data() {
    return {
      items: [],
    };
  },

  async created() {
    try {
      const response = await axios.get("http://localhost:8000/items");
      this.items = response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  },

  methods: {
    add_item(item_id) {
      const token = localStorage.getItem('token');

      axios.get("http://localhost:8000/protected_route", {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(response => {
          console.log(response.data);
          axios.post("http://localhost:8000/user/items", {
            "user_id": response.data.user.id,
            "item_id": item_id,
            "count": 1
          })
            .then(response => {
              console.log(response);
              this.itemStatus('Товар добавлен', '#5e9269','#2c3e50');
            })
            .catch(error => {
              console.error("Error fetching data:", error);
            });
        })
        .catch(error => {
          this.$router.push('/auth');
        });
    },

    itemStatus(text, blockColor, textColor) {
      let div = document.createElement("div");
      div.innerHTML = `
          <div>
            ${text}
          </div>
      `;
      div.setAttribute(
        "style",
        `
        background-color: ${blockColor};

        border-radius: 10px;
        
        color: ${textColor};

        padding: 15px 20px;
        margin-top: 20px;

        animation: blockAppearance 700ms ease;
      `
      );

      let wrapper = document.getElementsByClassName("statusBlock_wrapper")[0];

      wrapper.append(div);

      setTimeout(() => div.remove(), 600);
    },
  }
};
</script>

<style scoped lang="scss">
.statusBlock_wrapper {
  display: flex;
  flex-direction: column;
  justify-content: end;
  align-items: center;

  font-family: "Inter", sans-serif;

  position: absolute;
  right: 50px;
  bottom: 30px;
}

.items {
  display: flex;
  justify-content: space-around;
  align-items: center;

  margin: 0 auto;

  width: 90vw;

  .item {
    background-color: rgba(94, 146, 105, 0.5);
    border-radius: 10px;
    cursor: pointer;

    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;

    overflow-y: hidden;

    width: 18%;
    height: 100px;

    .data {
      background-color: #5e9269;

      display: flex;
      justify-content: space-between;
      align-items: center;

      font-family: "Inter", sans-serif;

      padding: 0 20px;

      height: 100%;
      width: 100%;

      .name {
        font-size: 2em
      }
    }
  }
}
</style>
