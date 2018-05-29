<style lang="scss" scoped>
  @import '../../common/style/varibles.scss';

  %flex-one {
    flex: 1;
  }

  .container,
  .service,
  .detail {
    @extend %flex-one;
  }

  .container-list .container-icon{
    float: right;
    svg {
      color: $table-th-icon-down-color;
    }
  }

  .output-btn svg {
    color: #aab2bd;
  }

  .container-tr td:nth-child(-n+3) {
    @extend %flex-one;
  }

  .output-td {
    position: relative;
  }

  .output-btn {
    float: right;
    margin-left: 5px;
    line-height: 1;
  }

  .status-icon {
    &__success {
      fill: $green;
      color: $green;
    }
    &__error {
      fill: $red;
      color: $red;
    }
    &__waiting {
      fill: $blue;
      color: $blue;
    }
  }

  .status-icon.padding {
    animation: circle 1s linear infinite;
  }

  .time-td {
    flex: none;
    width: 120px;
  }

  .status-td {
    flex: none;
    width: 90px;
  }

  @keyframes circle {
    0 {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
<template>
  <div class="container-list">
    <StyleTable :height="this.tableHeight">
      <tr slot="head">
        <th class="detail">
          <span>作业</span>
        </th>
        <th class="container">
          <span>容器</span>
        </th>
        <th class="service">
          <span>服务</span>
        </th>
        <th class="log">
          <span>日志</span>
        </th>
        <th class="status-td">
          <span>状态</span>
        </th>
        <th class="time-td">
          <span>执行时间</span>
        </th>
      </tr>
      <template slot="body">
        <tr class="container-tr"
          v-for="(container, index) in containerList">
          <td v-if="container.name">
            {{container.JobName}}
          </td>
          <td v-if="container.name">
            {{container.name}}
          </td>
          <td v-if="container.name">
            {{container.service}}
          </td>
          <td
            class="output-td"
            v-if="container.name"
            @click="onHandleClickTr(index)">
            <span class="output-btn">
              <svg class="icon output-icon" :viewBox="iconGoto.viewBox">
                <use :xlink:href="`#${iconGoto.id}`" >
                </use>
              </svg>
            </span>
            {{transformOutput(container)}}
          </td>
          <td class="status-td" v-if="container.name">
            <!-- running -->
            <svg v-if="isRunningStatus(container)" class="status-icon padding">
              <use xlink:href="#icon_circle-rotate"></use>
            </svg>
            <span v-if="isRunningStatus(container)" :class="getStatus(container).class">
              执行中
            </span>
            <!-- 其他 -->
            <svg v-if="!isRunningStatus(container)" class="status-icon" :class="getStatus(container).class">
              <use xlink:href="#icon_status-dot"></use>
            </svg>
            <span v-if="!isRunningStatus(container)" :class="getStatus(container).class">
              {{getStatus(container).msg}}
            </span>
          </td>
          <td class="time-td" v-if="container.name">
            {{container.StartTime === 0 ? '-' : transformTime(container.StartTime)}}
          </td>
        </tr>
      </template>
    </StyleTable>
  </div>
</template>
<script>
  import StyleTable from '../styleTable/StyleTable';
  import Utils from '../../utils';
  import iconGoto from '../../assets/icon_goto.svg';

  export default {
    name: 'ContainerList',
    props: {
      containers: {
        type: Array,
        default: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      },
      curJob: {
        type: Object,
      },
    },
    data() {
      return {
        tableHeight: 10,
        iconGoto,
      };
    },
    computed: {
      containerList() {
        let tempList = [];

        for (let i = 0; i < this.tableHeight; i += 1) {
          tempList.push(0);
        }

        const sortContainers = this.containers;
        this.containers.forEach((item) => {
          const start = item.StartTime;
          this.transformTime(start);
        });

        if (this.containers.length > this.tableHeight) {
          tempList = sortContainers;
        } else {
          sortContainers.forEach((item, idx) => {
            tempList[idx] = item;
          });
        }
        return tempList;
      },
    },
    methods: {
      transformTime(time) {
        return Utils.timeConverter(time);
      },
      onHandleClickTr(index) {
        if (!this.containerList[index]) return;
        this.$emit('selectCon', index);
      },
      getStatus(container) {
        let result = {
          class: 'status-icon__error',
          msg: '失败',
        };
        const { Status, ExitCode } = container;
        if (Status === 'STARTING' || Status === 'CREATED') {
          result = {
            class: 'status-icon__waiting',
            msg: '等待中',
          };
        } else if (Status === 'FINISHED') {
          if (ExitCode === 0) {
            result = {
              class: 'status-icon__success',
              msg: '成功',
            };
          }
        }
        return result;
      },
      isRunningStatus(container) {
        return container.Status && container.Status === 'RUNNING';
      },
      transformOutput({ Output, Status, E }) {
        // 失败
        if (Status === 'CREATE_FAILED' || Status === 'RUNNING_FAILED') {
          return E;
        }
        if (!Output) return '';
        const outPutList = Output.split('\n').reverse();
        const idx = outPutList.findIndex(item => item && item.trim() !== '');
        return outPutList[idx];
      },
    },
    components: {
      StyleTable,
    },
  };
</script>
