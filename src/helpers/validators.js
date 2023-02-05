export function numberValidator(value, minN, maxN, canBeNull = true) {
  if (canBeNull && !value) {
    return true;
  }
  let isValid = true;
  if (value < minN || value > maxN) {
    isValid = false;
  }
  return isValid;
}

export const zerosNumberValidator = (value) => numberValidator(value, 0, 11, true);
export const qRsNumberValidator = (value) => numberValidator(value, 0, 1000000);

export const prefixValidator = (value) => {
  let isValid = true;
  if (value.length > 20) {
    isValid = false;
  }
  return isValid;
};

export const suffixValidator = (value) => prefixValidator(value);
