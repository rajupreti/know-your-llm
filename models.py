import urllib.request
import json

PROVIDERS = {
    "GLM": "zai-org",
    "ByteDance": "ByteDance-Seed",
    "Google": "google",
    "Kimi": "moonshotai",
    "OpenAI": "openai",
    "Meta": "meta-llama",
    "DeepSeek": "deepseek-ai",
    "Alibaba Cloud": "Qwen",
    "Mistral AI": "mistralai",
    "Microsoft": "microsoft",
    "NVIDIA": "nvidia",
    # "Cohere": "CohereForAI", #disabled for now
}


def fetch_models_for_author(author, limit=50):
    url = f"https://huggingface.co/api/models?author={author}&sort=downloads&limit={limit}"

    request = urllib.request.Request(
        url, 
        headers={
            "User-Agent": "know-your-llm/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode())


def fetch_model_details(model_id):
    url = f"https://huggingface.co/api/models/{model_id}"
    
    request = urllib.request.Request(
        url, 
        headers={
            "User-Agent": "know-your-llm/1.0"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode())
        used_storage = data.get("usedStorage")
        return {
            "model_id": model_id,
            "parameters": data.get("safetensors", {}).get("total"),
            "disk_size_gb": round(used_storage / 1024**3, 2) if used_storage else None,
            "license": data.get("cardData", {}).get("license"),
            "gated": data.get("gated"),
            "likes": data.get("likes"),
        }
    except Exception:
        return {"model_id": model_id, "parameters": None, "disk_size_gb": None, "license": None, "gated": None, "likes": None}

# made with claude
def fetch_all_models():
    all_models = []
    num_providers = len(PROVIDERS)

    for provider_index, (provider_name, author) in enumerate(PROVIDERS.items(), start=1):
        try:
            models = fetch_models_for_author(author)
        except Exception as e:
            print(f"[{provider_index}/{num_providers}] Failed to fetch {provider_name}: {e}")
            continue

        num_models = len(models)
        print(f"[{provider_index}/{num_providers}] {provider_name}: {num_models} models")

        for model_index, m in enumerate(models, start=1):
            model_id = m.get("id")
            print(f"    ({model_index}/{num_models}) {model_id}", end="\r")
            details = fetch_model_details(model_id)
            all_models.append({
                "provider": provider_name,
                "model": model_id,
                "parameters": details["parameters"],
                "disk_size_gb": details["disk_size_gb"],
                "license": details["license"],
                "gated": details["gated"],
                "downloads": m.get("downloads"),
                "likes": details["likes"],
            })
        print()
    return all_models


def main():
    models = fetch_all_models()
    models.sort(key=lambda m: m["downloads"] or 0, reverse=True)
    print()
    print("Fetched:", len(models))

    with open("models.json", "w", encoding="utf-8") as f:
        json.dump(models, f, indent=2)
    print(f"Saved to models.json")


if __name__ == "__main__":
    main()