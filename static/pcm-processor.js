class PCMProcessor extends AudioWorkletProcessor {

    process(inputs, outputs, parameters) {

        const input = inputs[0];

        if (input && input[0]) {

            const samples = input[0];

            const pcm = new Int16Array(samples.length);

            for (let i = 0; i < samples.length; i++) {

                let sample = samples[i];

                sample = Math.max(-1, Math.min(1, sample));

                pcm[i] =
                    sample < 0
                        ? sample * 32768
                        : sample * 32767;
            }

            this.port.postMessage(pcm.buffer);
        }

        return true;
    }
}

registerProcessor("pcm-processor", PCMProcessor);