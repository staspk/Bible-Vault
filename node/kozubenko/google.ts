export function GOOGLE_VM_EXTERNAL_IP() {
    return fetch(
        "http://169.254.169.254/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip", {
            headers: { "Metadata-Flavor": "Google" }
        }
    ).then(res => res.text());
}