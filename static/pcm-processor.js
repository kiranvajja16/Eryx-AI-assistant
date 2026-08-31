class PCMProcessor extends AudioWorkletProcessor {

    constructor() {
        super();

        this.bufferSize = 1600; // 100 ms at 16 kHz
        this.buffer = new Int16Array(this.bufferSize);
        this.bufferIndex = 0;
    }

    process(inputs, outputs, parameters) {

        const input = inputs[0];

        if (!input || !input[0]) {
            return true;
        }

        const samples = input[0];

        for (let i = 0; i < samples.length; i++) {

            let sample = samples[i];

            sample = Math.max(-1, Math.min(1, sample));

            const pcmSample =
                sample < 0
                    ? sample * 32768
                    : sample * 32767;

            this.buffer[this.bufferIndex] = pcmSample;
            this.bufferIndex++;

            // Buffer full → send ~100 ms
            if (this.bufferIndex >= this.bufferSize) {

                const chunk = this.buffer.buffer.slice(0);

                this.port.postMessage(chunk, [chunk]);

                this.buffer = new Int16Array(this.bufferSize);
                this.bufferIndex = 0;
            }
        }

        return true;
    }
}

registerProcessor("pcm-processor", PCMProcessor);