const cd = (currPath, newPath) => {
    if (newPath[0] === '/') {
        return newPath
    }
    if (newPath === '.') {
        return currPath
    }
    const currPathArr = currPath.split('/') // looks like ['', 'a', 'b', 'c', 'd']
    const newPathArr = newPath.split('/') // looks like ['..', '..', 'x']
    const finalPath = []
    for (let i = 0; i < newPathArr.length; i++) {
        if (newPathArr[i] === '..') {
            currPathArr.pop()
        } else {
            finalPath.push(newPathArr[i])
        }
    }
    return currPathArr.join('/') + '/' + finalPath.join('/')
}

console.log(cd('/a/b/c/d', '../x')) // '/a/b/c/x'
console.log(cd('/a/b/c/d', '../../x')) // '/a/b/x'
console.log(cd('/a/b/c/d', '/x')) // '/x'
console.log(cd('/a/b/c/d', '/a/b/c/d')) // '/a/b/c/d'
console.log(cd('/a/b/c/d', '/a/b/c/d/e')) // '/a/b/c/d/e'
console.log(cd('/a/b/c/d', '..')) // '/a/b/c'
console.log(cd('/a/b/c/d', '../..')) // '/a/b'
console.log(cd('/a/b/c/d', '.')) // '/a/b/c/d'
console.log(cd('/a/', '../..')) // '/'

class RateLimiter {
    constructor(maxRequests) {
        this.history = [];
        this.maxRequests = maxRequests;
    }

    shouldProcess(requestTime) {
        this.history = this.history.filter((req) => req > requestTime - 1000);
        if (this.history.length < this.maxRequests) {
            this.history.push(requestTime);
            return true;
        } else {
            return false;
        }
    }
}

async function mapLimits(inputs, limit, iteratee, finalCallback) {
    const queue = [...inputs]; // Create a copy to avoid modifying input
    const results = new Array(inputs.length); // Store results in order
    let activeOperations = 0;
  
      const tryProcessNext = async () => {
          while (queue.length > 0 && activeOperations < limit) {
            const value = queue.shift();
            const index = inputs.indexOf(value);
  
            activeOperations++;
              
            try {
                const result = await iteratee(value);
                results[index] = result;
            }
            catch (error) {
                console.error(`Error processing ${value}: `, error);
                results[index] = error;
            }
            finally {
                 activeOperations--;
              }
              tryProcessNext(); // continue processing if not finished.
          }
          if (queue.length === 0 && activeOperations === 0) {
             finalCallback(); //resolve the promise if all items have been processed
          }
      }
      
      tryProcessNext(); //start processing
    return results;
  }

async function exampleAsyncFunction(value) {
    return new Promise(resolve => {
        setTimeout(() => {
           console.log(`Processing value ${value}`);
           resolve(value * 2);
        }, Math.random() * 1000);
    });
}

const inputArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const finalCallback = () => {
    console.log("All items have been processed.");
};

async function runExample() {
  const results = await mapLimits(inputArray, 2, exampleAsyncFunction, finalCallback);
  console.log("Final Results:", results);
}

runExample();
