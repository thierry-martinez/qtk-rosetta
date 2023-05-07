terraform {
  required_providers {
    cloudstack = {
      source  = "cloudstack/cloudstack"
      version = "0.4.0"
    }
  }
}

provider "cloudstack" {
  api_url = "https://sesi-cloud-ctl1.inria.fr/client/api"
  timeout = 1200
}

variable "GITHUB_TOKEN" {
  type = string
}

variable "SSH_PUBLIC_KEY" {
  type = string
}

resource "cloudstack_instance" "ubuntu" {
  count = 3
  ## It is a good practice to have the "{project name}-" prefix
  ## in VM names.
  name             = format("qat-github-runner-%d", count.index)
  service_offering = "Custom"
  template         = "ubuntu-2204-64-server"
  zone             = "zone-ci"
  details = {
    cpuNumber = 16
    memory    = 16000
  }
  expunge = true
  user_data = templatefile("cloud-init.yaml.tftpl", {
    GITHUB_TOKEN = var.GITHUB_TOKEN
    SSH_PUBLIC_KEY     = var.SSH_PUBLIC_KEY
  })
}
