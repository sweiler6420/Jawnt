import { useEffect, useRef } from 'react';

const usePoll = (callback, interval = 10000, options = {}) => {
  const { immediate = false } = options;
  const savedCallback = useRef();

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (immediate && savedCallback.current) {
      savedCallback.current();
    }

    const tick = () => {
      if (savedCallback.current) {
        savedCallback.current();
      }
    };

    const id = setInterval(tick, interval);
    return () => clearInterval(id);
  }, [interval, immediate]);
};

export default usePoll;
