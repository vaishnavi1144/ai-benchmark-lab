import json
from core.open_source_assistant import generate_response as open_ai
from core.frontier_assistant import generate_response as frontier_ai
from core.evaluator import evaluate_response

def run_benchmark():
    with open("data/test_prompts.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)

    results = []

    print("🚀 Running AI Benchmark...\n")

    for i, prompt in enumerate(prompts):
        print(f"Testing {i+1}/{len(prompts)}: {prompt}")

        try:
            oss_response = open_ai(prompt, [])
            frontier_response = frontier_ai(prompt, [])

            oss_scores = evaluate_response(prompt, oss_response)
            frontier_scores = evaluate_response(prompt, frontier_response)

            results.append({
                "prompt": prompt,
                "oss_response": oss_response,
                "frontier_response": frontier_response,
                "oss_scores": oss_scores,
                "frontier_scores": frontier_scores
            })

        except Exception as e:
            print("Error:", e)

    print("\n✅ Benchmark Completed!")

    return results


if __name__ == "__main__":
    run_benchmark()