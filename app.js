const display = document.getElementById('display');
const history = document.getElementById('history');
const buttons = document.querySelectorAll('.button');

const state = {
  value: '0',
  operator: null,
  previousValue: null,
  waitingForOperand: false,
  lastAction: null,
};

const updateDisplay = () => {
  display.textContent = state.value;
  history.textContent = state.operator ? `${state.previousValue || ''} ${formatOperator(state.operator)}` : '';
};

const formatOperator = (operator) => {
  return ({ add: '+', subtract: '−', multiply: '×', divide: '÷' })[operator] || '';
};

const inputDigit = (digit) => {
  if (state.waitingForOperand) {
    state.value = digit;
    state.waitingForOperand = false;
  } else {
    state.value = state.value === '0' ? digit : state.value + digit;
  }
};

const inputDecimal = () => {
  if (state.waitingForOperand) {
    state.value = '0.';
    state.waitingForOperand = false;
    return;
  }
  if (!state.value.includes('.')) {
    state.value += '.';
  }
};

const handleOperator = (nextOperator) => {
  const value = parseFloat(state.value);

  if (state.operator && state.waitingForOperand) {
    state.operator = nextOperator;
    return;
  }

  if (state.previousValue == null) {
    state.previousValue = value;
  } else if (state.operator) {
    const result = calculate(state.previousValue, value, state.operator);
    state.previousValue = result;
    state.value = String(result);
  }

  state.waitingForOperand = true;
  state.operator = nextOperator;
};

const calculate = (left, right, operator) => {
  if (operator === 'add') return left + right;
  if (operator === 'subtract') return left - right;
  if (operator === 'multiply') return left * right;
  if (operator === 'divide') return right === 0 ? 'Error' : left / right;
  return right;
};

const clearAll = () => {
  state.value = '0';
  state.operator = null;
  state.previousValue = null;
  state.waitingForOperand = false;
  state.lastAction = null;
};

const toggleSign = () => {
  if (state.value === '0') return;
  state.value = state.value.startsWith('-') ? state.value.slice(1) : `-${state.value}`;
};

const applyPercent = () => {
  const value = parseFloat(state.value);
  state.value = String(value / 100);
};

const handleEquals = () => {
  const value = parseFloat(state.value);

  if (state.operator == null || state.previousValue == null) {
    return;
  }

  const result = calculate(state.previousValue, value, state.operator);
  state.value = String(result);
  state.previousValue = null;
  state.operator = null;
  state.waitingForOperand = true;
};

buttons.forEach((button) => {
  button.addEventListener('click', () => {
    const { action, digit } = button.dataset;

    if (digit) {
      inputDigit(digit);
    } else if (action) {
      switch (action) {
        case 'clear':
          clearAll();
          break;
        case 'toggle-sign':
          toggleSign();
          break;
        case 'percent':
          applyPercent();
          break;
        case 'decimal':
          inputDecimal();
          break;
        case 'equals':
          handleEquals();
          break;
        case 'add':
        case 'subtract':
        case 'multiply':
        case 'divide':
          handleOperator(action);
          break;
      }
    }
    updateDisplay();
  });
});

updateDisplay();
