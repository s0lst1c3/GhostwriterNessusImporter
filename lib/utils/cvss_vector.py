from lib.types.cvss_vector import CVSSVectorPrefixes


def vector_prefix(value: str):

    if ":" not in value:
        raise ValueError(f"Invalid CVSS vector: {value}")

    if "#" in value:
        value = value.split("#")[1]

    value = value.replace("CVSS", "")
    value = value.replace("#", "")
    value = value.split(":")[0]

    return value.strip("/").upper()


def vector_value(prefix: str, value: str):
    return ":".join([prefix, value.split(":")[1].upper().strip("/")])


def process_cvss_vector(parts: list[str]):

    attack_vector = "AV:P"
    attack_complexity = "AC:L"
    privileges_required = "PR:N"
    user_interaction = "UI:N"
    scope = "S:U"
    confidentiality_impact = "C:N"
    integrity_impact = "I:N"
    availability_impact = "A:N"

    for vector in parts:
        if vector.upper().startswith("CVSS"):
            continue
        p = vector_prefix(vector)
        match p:
            case CVSSVectorPrefixes.ATTACK_VECTOR:
                attack_vector = vector_value("AV", vector)
            case CVSSVectorPrefixes.ATTACK_COMPLEXITY:
                attack_complexity = vector_value("AC", vector)
            case (
                CVSSVectorPrefixes.PRIVILEGES_REQUIRED
                | CVSSVectorPrefixes.AUTH_REQUIRED
            ):
                privileges_required = vector_value("PR", vector)
            case CVSSVectorPrefixes.USER_INTERACTION:
                user_interaction = vector_value("UI", vector)
            case CVSSVectorPrefixes.SCOPE:
                scope = vector_value("S", vector)
            case CVSSVectorPrefixes.CONFIDENTIALITY_IMPACT:
                confidentiality_impact = vector_value("C", vector)
            case CVSSVectorPrefixes.INTEGRITY_IMPACT:
                integrity_impact = vector_value("I", vector)
            case CVSSVectorPrefixes.AVAILABILITY_IMPACT:
                availability_impact = vector_value("A", vector)
            case _:
                raise ValueError(f"Invalid CVSS vector prefix: {p} for vector {vector}")
    return "/".join(
        [
            "CVSS:3.1",
            attack_vector,
            attack_complexity,
            privileges_required,
            user_interaction,
            scope,
            confidentiality_impact,
            integrity_impact,
            availability_impact,
        ]
    )
