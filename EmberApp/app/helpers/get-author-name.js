import { helper } from '@ember/component/helper';
import { htmlSafe } from '@ember/string';

export function getAuthorName(params/*, hash*/) {
  let [firstName, lastName] = params;
  return htmlSafe(`<strong>${lastName}</strong> ${firstName}`);
}

export default helper(getAuthorName);
