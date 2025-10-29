# InfinityStyleVerse AI Stylist 

## Model Used
- **Name**: The `transformers` library by Hugging Face is used, using the **"gpt2"** model for text generation as instructed. This is a general-purpose language model with 124 million parameters.
- **Device**: The model runs on the CPU by default (`device=-1`). If a CUDA-enabled GPU is available, it uses `device=0` for faster processing.
- **Configuration**: The model generates text with a maximum of 80 new tokens (`max_new_tokens=80`) and enables truncation to handle longer inputs efficiently.

## Sample Inputs and Outputs
### Input Format
The API accepts POST requests to the `/api/style-advice` endpoint with a JSON body containing a `question` key. For example:
- `{"question": "What should I wear for a night out in Paris?"}`
- `{"question": "How to style a black denim jacket?"}`

### Output Format
The API returns a JSON response with an `advice` field which contains the generated text, tagged with emojis for several clothing items defined in a dictionary, or an `error` field if the request fails. Examples:

#### Sample 1
- **Input**: `{"question": "What to wear for a summer party?"}`
- **Output**: `{"advice": "You are a helpful AI fashion stylist. What to wear for a summer party? What to wear for a weekend or weekend retreat? What to wear for an evening or evening retreat? What to wear for a dinner party? What to wear for a dinner party? What to wear for a weekend or weekend retreat? What to wear for a weekend or weekend retreat? What to wear for a birthday party? What to wear for a birthday party?"}`

#### Sample 2
- **Input**: `{"question": "Suggest an outfit with a jacket and trousers."}`
- **Output**: `{"advice": "You are a helpful AI fashion stylist. Suggest an outfit with a jacket 🧥 and trousers 👖 and gloves 🧤 to help you out and make your wardrobe fit. Or, if you're a designer, let me know. If you're a designer looking to make an investment, or you're looking to add a unique style to your wardrobe, please use my tip below.."}`

#### Sample 3
- **Input**: `{"question": "Give me a casual look with shorts and a shirt."}` 
- **Output**: `{"advice": "You are a helpful AI fashion stylist. Give me a casual look with shorts 🩳 and a shirt 👕. That's 👒 what you are looking for. But what if you're not looking for the casual look? There are a few choices. I'm going to go with the classic, classic and casual look. The classic look is what you get when you get the casual look. But what if you're looking for something more casual that will make you feel more comfortable in the house?."}`

## Limitations
- **Model Accuracy**: The "gpt2" model is a general-purpose language model which is not specifically trained for fashion advice. Responses lack context-specific detail and it suggests inappropriate text like the samples provided above.
- **Vocabulary Constraints**: The emoji tagging is limited to a predefined dictionary (`clothing_emojis`), so unrecognized clothing items (e.g., "socks," "belt") won’t receive emojis.
- **Performance**: On a CPU, generation takes around 5 seconds per request, which can be acceptable but could improve with GPU support.
- **Input Sensitivity**: The API requires a valid JSON body with a `question` key. Missing keys would give 400 errors.
- **Output Length**: The `max_new_tokens=80` limit may truncate longer responses, which cuts off advice. Increasing this could increase the time delay.
- **Error Handling**: Even though error handling was improved, rare server-side issues (eg: model loading failures) may still occur, giving 500 errors.

## Future Improvements
- Can fine-tune the "gpt2" model on a fashion-specific dataset for more accuracy.
- Can expand the `clothing_emojis` dictionary to include more items.
- Implementing GPU support or a cloud-based API will more faster responses.
