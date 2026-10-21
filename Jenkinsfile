boolean disableIndexTriggers = env.BRANCH_NAME != 'main'

quadletPipeline(
    disableIndexTriggers: disableIndexTriggers,
    podmanSecretMappings: [
        [
            type: 'string',
            credentialsId: 'mqtt-password-file',
            podmanSecretStringName: 'mqtt_password_file'
        ]
    ]
)
