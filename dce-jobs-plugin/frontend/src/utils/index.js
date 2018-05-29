import Noty from 'noty';

export default {
  createNoty(text, type) {
    return new Noty({
      text,
      layout: 'topRight',
      theme: 'relax',
      type,
      timeout: 1000,
    }).show();
  },
  /* eslint-disable */
  timeConverter(UNIX_timestamp){
    const a = new Date(UNIX_timestamp * 1000);
    const months = ['1','2','3','4','5','6','7','8','9','10','11','12'];
    const year = a.getFullYear();
    const month = months[a.getMonth()];
    const date = a.getDate();
    const hour = a.getHours();
    const min = a.getMinutes();
    const sec = a.getSeconds();
    const time = `${year}/${month}/${date} ${hour < 10 ? '0' : ''}${hour}:${min < 10 ? '0' : ''}${min}`;
    return time;
  },
};
