<style lang="scss" scoped>
@import '../../common/style/varibles.scss';

%flex-two {
  flex: 2;
}

.table-wrap.dao-table.slat {
  font-size: 14px;

  tbody tr,
  thead tr {
    height: $table-row-height;
    line-height: $table-row-height;  
  }

  th,
  td {
    margin: auto 0;
    padding-left: 10px;
    // overflow: hidden;
  }

  .body tr {
    border-bottom: none;

    &:nth-child(odd),
    &:nth-child(odd):hover {
      background-color: $table-th-bg;
    }

    &:nth-child(even),
    &:nth-child(even):hover {
      background-color: $table-row-bg-color;
    }

    td {
      &:last-child {
        text-align: left;
      }
    }

    &.active,
    &.active:hover {
      background-color: #096dec;
      &>td {
        color: #fff;
      }
    }
  }
}

.head {
  font-family: PingFangSC-Regular;
  font-size: 14px;
  color: #595F69;
  line-height: 24px;

  tr {
    background-color: $table-th-bg;
  }

  th {
    box-shadow: 0 1px 0 0 #E4E7ED, 1px 0 0 0 #E4E7ED, 0 -1px 0 0 #E4E7ED;

    svg {
      color: $table-th-icon-color;
      margin-right: 10px;     
    }
  }
}
</style>
<template>
  <div class="dao-table-main">
    <table class="dao-table slat table-wrap">
      <thead class="head">
        <slot name="head">
        </slot>
      </thead>
      <tbody class="body" :style="{height: bodyHeight}">
        <slot name="body">
          <tr v-for="n in height"></tr>
        </slot>
      </tbody>
    </table>
  </div>
</template>
<script>
  export default {
    name: 'styleTable',
    props: {
      height: Number,
    },
    data() {
      return {
        bodyHeight: `${this.height * 30}px` || '300px',
      };
    },
    methods: {
    },
  };
</script>
