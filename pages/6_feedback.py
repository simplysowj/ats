import streamlit as st

class FeedbackApp:
    def __init__(self):
        self.feedback = []

    def collect_feedback(self, rating, comment):
        self.feedback.append({'rating': rating, 'comment': comment})

    def display_feedback_form(self):
        st.subheader("Feedback Form")
        rating = st.slider("Rate your experience (1 - 5)", min_value=1, max_value=5, step=1)
        comment = st.text_area("Leave any comments or suggestions")
        if st.button("Submit Feedback"):
            self.collect_feedback(rating, comment)
            st.success("Thank you for your feedback!")

    def display_feedback_analysis(self):
        st.subheader("Feedback Analysis")
        if self.feedback:
            for idx, entry in enumerate(self.feedback, start=1):
                st.write(f"Feedback #{idx}:")
                st.write(f"Rating: {entry['rating']}")
                st.write(f"Comment: {entry['comment']}")
        else:
            st.write("No feedback has been provided yet.")

def main():
    app = FeedbackApp()
    st.title("Chatbot Feedback App")
    app.display_feedback_form()
    app.display_feedback_analysis()

if __name__ == "__main__":
    main()
