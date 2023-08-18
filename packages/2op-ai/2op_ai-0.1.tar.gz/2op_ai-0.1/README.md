This is a continually-updated market data analysis machine learning transformer model intended for summarizing & interpreting market & economic data. 
To use:
1. gh repo clone sscla1/2op_ai
2. install requirements.txt wherever running your application
3. import statement: from 2op_ai import ai_pipeline
4. use case for summarizer & interpreter
    def summarize_text(self, text):
        """
        Summarizes the provided text.

        Args:
            text (str): The text to be summarized.

        Returns:
            str: The summarized text.
        """
        try:
            # Perform text summarization using AI pipeline
            summary = self.ai_pipeline(text, max_length=600)[0]['summary_text']
            return summary

        except Exception as e:
            logging.error(f"An error occurred when trying to summarize text: {e}")
            return ""

    def generate_interpretation(self, summary):
        """
        Generates interpretation for the summary using the AI pipeline.

        Args:
            summary (str): The summary to generate interpretation for.

        Returns:
            str or None: The generated interpretation or None if an error occurs.
        """
        logging.info("Attempting to generate interpretation.")
        try:
            input_text = "Explain the provided data, its affect on the market, and specific sectors, in layman's terms, in 300 words or less: " + summary
            interpretation = self.ai(input_text, max_length=300, do_sample=True)[0]['generated_text']
            return interpretation
        except Exception as e:
            logging.error(f"An error occurred when trying to generate interpretation: {e}")
            return None