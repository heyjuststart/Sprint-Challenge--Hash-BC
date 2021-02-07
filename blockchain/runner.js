const { spawn } = require('child_process');
const kill = require('tree-kill');
const axios = require('axios');
const state = {
  last_proof: null,
  num_children: 3,
  children: [],
  proof_history: new Set([]),
  id: '🤘🤘🤘🤘🤘c089db227bf02d79fc2🤘🤘🤘🤘🤘',
  coin_count: 0,
  timeout: null,
  check_interval: 2000
};

const stop_miners = () => {
  console.log('Stopping Miners');
  for (let i = 0; i < state.children.length; i++) {
    console.log(`Ending child ${i}`);
    // state.children[i].stdin.pause();
    // state.children[i].kill('SIGINT');
    // state.children[i].disconnect();
    kill(state.children[i].pid, 'SIGKILL');
  }
};

const restart_miners = last_proof => {
  // stop any running children
  stop_miners();

  // dereference those killed processes
  state.children = [];

  console.log('Restarting Miners');
  // spawn a number of child processes with the current last_proof
  for (let i = 0; i < state.num_children; i++) {
    // spawn 'command', [...arguments]
    const this_child = spawn('python', [
      'proofer.py',
      last_proof,
      i,
      state.num_children
    ]);

    // on stdout, a miner found a solution
    // stop all miners
    // post solution and restart
    this_child.stdout.once('data', data => {
      console.log(`Output from miner ${i}:`, data.toString().trim());
      stop_miners();
      proof = data.toString().trim();
      axios
        .post('http://lambda-coin-test-1.herokuapp.com/mine', {
          id: state.id,
          proof
        })
        .then(res => {
          if (res.data.message === 'New Block Forged') {
            state.coin_count += 1;
            console.log(`############# Won the race! ${state.coin_count} ##################################`);
          } else {
            console.log('************* NOPE *****************');
          }
          check_last_proof();
        });
    });
  }
};

const check_last_proof = () => {
  console.log('Checking Last Proof');
  if (state.timeout !== null) {
    // cancel the timeout
    clearTimeout(state.timeout);
    state.timeout = null;
  }

  return axios
    .get('http://lambda-coin-test-1.herokuapp.com/last_proof')
    .then(res => {
      const { proof: last_proof } = res.data;

      // if last_proof is null, this is the first run
      // or if we haven't seen this proof yet (lost the marathon, try again)
      if (last_proof === null || last_proof !== state.last_proof) {
        console.log('New Proof!');
        restart_miners(last_proof);
      }

      // update state
      state.last_proof = res.data.proof;
      state.proof_history.add(state.last_proof);

      // set the timeout for the next update
      state.timeout = setTimeout(check_last_proof, state.check_interval);
    });
};

// Start the process
check_last_proof();
