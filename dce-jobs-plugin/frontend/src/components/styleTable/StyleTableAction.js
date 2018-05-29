export default {
/**
 *
 * @param  {[Array]} data   [需要填入的原始数据]
 * @param  {[type]} height [table 的高度]
 * @return {[type]}        [description]
 */

/* eslint-disable */
  init(datas, height) {
    let tempData = [];
    if (datas.length >= height) {
      tempData = datas.map(item => this.transformObject(item));
    } else {
      for (let i = 0; i < height; i++) {
        if (!datas[i]) {
          tempData.push(0);
        } else {
          tempData.push(this.transformObject(datas[i]));
        }
      }
    }
    return tempData;
  },
  addItem(curDatas, data, height) {
    const tempData = curDatas;
    if (curDatas.length > height) {
      tempData.push(data);
    } else {
      const relaLength = this.detectLength(curDatas, height);
      if (relaLength < height) {
        tempData[relaLength] = data;
      } else {
        tempData.push(data);
      }
    }

    return tempData;
  },

  reduceItem(curDatas, index, height) {
    if (!curDatas[index]) return;
    const temp = curDatas;
    const len = this.detectLength(curDatas, height);

    temp.splice(index, 1);
    const rest = height - len;
    /* eslint-disable no-plusplus */
    for (let i = 0; i < rest; i++) {
      temp.push(0);
    }

    return temp;
  },

  detectLength(list, height) {
    const idx = list.indexOf(0);
    if (idx >= 0 && idx <= height - 1) {
      return idx;
    }
    return list.length;
  },
  transformObject(data) {
    if (Object.prototype.toString.call(data) === '[object Object]') {
      return {
        ...data,
      };
    }
    return data;
  },
}
