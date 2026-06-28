const API_URL = 'http://localhost:5000/api/calc';
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

const apiRequest = async (payload) => {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'API error');
  }
  return data.result;
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

const handleOperator = async (nextOperator) => {
  const value = parseFloat(state.value);

  if (state.operator && state.waitingForOperand) {
    state.operator = nextOperator;
    return;
  }

  if (state.previousValue == null) {
    state.previousValue = value;
  } else if (state.operator) {
    const result = await apiRequest({
      action: state.operator,
      left: state.previousValue,
      right: value,
    });
    state.previousValue = result;
    state.value = String(result);
  }

  state.waitingForOperand = true;
  state.operator = nextOperator;
};

const calculate = async (left, right, operator) => {
  return await apiRequest({ action: operator, left, right });
};

const clearAll = () => {
  state.value = '0';
  state.operator = null;
  state.previousValue = null;
  state.waitingForOperand = false;
  state.lastAction = null;
};

const toggleSign = async () => {
  if (state.value === '0') return;

  const result = await apiRequest({
    action: 'toggle-sign',
    value: state.value,
  });
  state.value = String(result);
};

const applyPercent = async () => {
  const value = parseFloat(state.value);
  const result = await apiRequest({
    action: 'percent',
    value,
  });
  state.value = String(result);
};

const handleEquals = async () => {
  const value = parseFloat(state.value);

  if (state.operator == null || state.previousValue == null) {
    return;
  }

  const result = await calculate(state.previousValue, value, state.operator);
  state.value = String(result);
  state.previousValue = null;
  state.operator = null;
  state.waitingForOperand = true;
};

buttons.forEach((button) => {
  button.addEventListener('click', async () => {
    const { action, digit } = button.dataset;

    try {
      if (digit) {
        inputDigit(digit);
      } else if (action) {
        switch (action) {
          case 'clear':
            clearAll();
            break;
          case 'toggle-sign':
            await toggleSign();
            break;
          case 'percent':
            await applyPercent();
            break;
          case 'decimal':
            inputDecimal();
            break;
          case 'equals':
            await handleEquals();
            break;
          case 'add':
          case 'subtract':
          case 'multiply':
          case 'divide':
            await handleOperator(action);
            break;
        }
      }
    } catch (error) {
      state.value = 'Error';
      console.error(error);
    }

    updateDisplay();
  });
});

updateDisplay();
