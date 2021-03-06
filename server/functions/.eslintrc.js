module.exports = {
  root: true,
  env: {
    es6: true,
    node: true,
  },
  extends: ['eslint:recommended', 'google'],
  rules: {
    'linebreak-style': 0,
  },
  parser: 'babel-eslint',
};
