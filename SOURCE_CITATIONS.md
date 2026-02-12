# Source Citations Feature - Documentation

## 📚 View Sources Feature

The DocGenius app now includes a **"View Sources"** feature that shows exactly where the AI got its information from!

### How It Works:

1. **Ask a question** in the chat interface
2. **Get an answer** from the AI
3. **Click "📚 View Sources"** expander below the answer
4. **See detailed information** about each source document:
   - Source filename
   - Page number
   - Document type/category
   - Content preview (first 300 characters)

### Example:

**User Question:**
> "How many days of annual leave do employees get?"

**AI Answer:**
> "All full-time employees are entitled to 20 days of paid annual leave per year."

**Sources (Click to expand):**
```
📚 View Sources

Source 1: sample_policy.pdf (Page 1)
Type: leave_policy
Content Preview:
"All full-time employees are entitled to 20 days of paid 
annual leave per year. Leave requests must be submitted 
at least 2 weeks in advance..."

Source 2: sample_policy.pdf (Page 1)
Type: leave_policy
Content Preview:
"Introduction: This document outlines our company's 
leave policy for all employees..."
```

### Benefits:

✅ **Transparency** - See exactly where information comes from
✅ **Verification** - Check the original source if needed
✅ **Trust** - Confidence that answers are based on your documents
✅ **Context** - Understand the full context of each answer
✅ **Compliance** - Track which documents were referenced

### Technical Details:

- Retrieves top 5 most relevant chunks from vector database
- Shows metadata including filename, page, and policy type
- Content preview limited to 300 characters for readability
- Sources stored with each answer in chat history
- Expandable UI to keep interface clean

### Metadata Tracked:

The system automatically tracks:
- `source`: PDF filename
- `page`: Page number in the PDF
- `policy_type`: Categorized as leave_policy, privacy_policy, or general_policy
- Full text content of the chunk

This helps you understand not just WHAT the AI answered, but WHERE it found that information!
