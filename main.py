import requests
import os

def make_request(url, authorization_key):
    headers = {
        "Authorization": authorization_key,
        "Content-Type": "application/json"
    }
    body = {
        "id": "e653dfed-4fec-425a-8272-9f888cc62684",
        "method": "get",
        "uri": "/buckets/blip_portal:builder_published_flow"
    }
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

def extract_camp(data):
    results = []
    if isinstance(data, dict):
        if data.get("type") == "ProcessHttp":
            results.append({
                "$title": data.get("$title", "N/A"),
                "method": data.get("settings", {}).get("method", "N/A"),
                "uri": data.get("settings", {}).get("uri", "N/A")
            })
        for value in data.values():
            results.extend(extract_camp(value))
    elif isinstance(data, list):
        for item in data:
            results.extend(extract_camp(item))
    return results

def save_results(results, subbot_name):
    output_file = f"{subbot_name}.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        for result in results:
            file.write(f"$title: {result['$title']}\n")
            file.write(f"method: {result['method']}\n")
            file.write(f"uri: {result['uri']}\n")
            file.write("-" * 40 + "\n")
    return output_file

def main():
    url = input("Por favor, insira a URL (ex: https://nome-do-contrato-): ")
    num_subbots = int(input("Quantos subbots você deseja processar? "))
    
    for i in range(num_subbots):
        subbot_name = input(f"Por favor, insira o nome do subbot {i + 1}: ")
        authorization_key = input(f"Por favor, insira a chave de autorização para o subbot {subbot_name}: ")
        
        data = make_request(url, authorization_key)
        if data:
            results = extract_camp(data)
            if results:
                print(f"Dados extraídos para o subbot '{subbot_name}':")
                for result in results:
                    print(f"$title: {result['$title']}")
                    print(f"method: {result['method']}")
                    print(f"uri: {result['uri']}")
                    print("-" * 40)
                output_file = save_results(results, subbot_name)
                print(f"Resultados para o subbot '{subbot_name}' salvos em '{output_file}'.")
            else:
                print(f"Nenhum dado foi extraído para o subbot '{subbot_name}'.")
        else:
            print(f"Erro ao processar o subbot '{subbot_name}'.")

if __name__ == "__main__":
    main()
